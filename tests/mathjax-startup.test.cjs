const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '..', 'script.js'), 'utf8');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const inlineScripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1]);
const headConfiguration = inlineScripts.find(source => source.includes('typeset: false'));
const lazyRendering = inlineScripts.find(source => source.includes('function lazyTypeset()'));

function fixture() {
    const listeners = [];
    const pending = [];
    const visible = [{}];
    const later = [{}];
    const observed = [];
    const typeset = [];
    const context = {
        document: {
            addEventListener(name, listener) {
                assert.equal(name, 'DOMContentLoaded');
                listeners.push(listener);
            },
            getElementById() { return null; },
            querySelectorAll(selector) {
                if (selector === 'section:nth-child(-n+4)') return visible;
                if (selector === 'section:nth-child(n+5)') return later;
                return [];
            }
        },
        console: { log() {}, error() {} },
        setTimeout(callback, delay) {
            assert.equal(delay, 500);
            pending.push(callback);
        },
        IntersectionObserver: class {
            constructor(callback) { this.callback = callback; }
            observe(section) { observed.push(section); }
            unobserve() {}
        }
    };
    context.window = context;
    vm.createContext(context);
    const engine = {
        typesetPromise(sections) {
            typeset.push(Array.from(sections));
            return Promise.resolve();
        },
        startup: { promise: Promise.resolve() }
    };
    return { context, listeners, pending, visible, later, observed, typeset, engine };
}

test('preserves head configuration before the asynchronous engine loads', () => {
    const state = fixture();
    vm.runInContext(headConfiguration, state.context);
    const configuration = state.context.MathJax;
    vm.runInContext(script, state.context);
    assert.equal(state.context.MathJax, configuration);
    assert.equal(state.context.MathJax.startup.typeset, false);
});

test('preserves a ready MathJax engine and renders without polling', () => {
    const state = fixture();
    vm.runInContext(headConfiguration, state.context);
    state.context.MathJax = state.engine;
    vm.runInContext(script, state.context);
    assert.equal(state.context.MathJax, state.engine);
    vm.runInContext(lazyRendering, state.context);
    state.listeners.forEach(listener => listener());
    assert.equal(state.pending.length, 0);
    assert.deepEqual(state.typeset, [state.visible]);
    assert.deepEqual(state.observed, state.later);
});

test('still polls and renders when the engine loads after the site script', () => {
    const state = fixture();
    vm.runInContext(headConfiguration, state.context);
    vm.runInContext(script, state.context);
    vm.runInContext(lazyRendering, state.context);
    state.listeners.forEach(listener => listener());
    assert.equal(state.pending.length, 1);
    assert.equal(state.typeset.length, 0);
    state.context.MathJax = state.engine;
    state.pending.shift()();
    assert.equal(state.pending.length, 0);
    assert.deepEqual(state.typeset, [state.visible]);
    assert.deepEqual(state.observed, state.later);
});

test('provides fallback configuration when the page has none', () => {
    const state = fixture();
    vm.runInContext(script, state.context);
    assert.equal(state.context.MathJax.tex.processEscapes, true);
    assert.equal(state.context.MathJax.tex.processEnvironments, true);
    assert.ok(state.context.MathJax.options.skipHtmlTags.includes('script'));
});

test('repeated site-script evaluation does not replace the ready engine', () => {
    const state = fixture();
    state.context.MathJax = state.engine;
    vm.runInContext(script, state.context);
    vm.runInContext(script, state.context);
    assert.equal(state.context.MathJax, state.engine);
});
