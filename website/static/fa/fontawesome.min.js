/*!
 * Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2024 Fonticons, Inc.
 */
!function() {
    "use strict";
    var t = () => {};
    let n = {}, e = {}, a = null, r = {
        mark: t,
        measure: t
    };
    try {
        "undefined" != typeof window && (n = window), "undefined" != typeof document && (e = document), 
        "undefined" != typeof MutationObserver && (a = MutationObserver), "undefined" != typeof performance && (r = performance);
    } catch (t) {}
    const {
        userAgent: i = ""
    } = n.navigator || {}, k = n, w = e, c = a;
    var o = r;
    const s = !!k.document, f = !!w.documentElement && !!w.head && "function" == typeof w.addEventListener && "function" == typeof w.createElement, u = ~i.indexOf("MSIE") || ~i.indexOf("Trident/");
    var l = "classic", m = "duotone", d = "sharp", p = "sharp-duotone", h = [ l, m, d, p ], g = {
        fak: "kit",
        "fa-kit": "kit"
    }, b = {
        fakd: "kit-duotone",
        "fa-kit-duotone": "kit-duotone"
    }, v = {
        classic: {
            fa: "solid",
            fas: "solid",
            "fa-solid": "solid",
            far: "regular",
            "fa-regular": "regular",
            fal: "light",
            "fa-light": "light",
            fat: "thin",
            "fa-thin": "thin",
            fad: "duotone",
            "fa-duotone": "duotone",
            fab: "brands",
            "fa-brands": "brands"
        },
        sharp: {
            fa: "solid",
            fass: "solid",
            "fa-solid": "solid",
            fasr: "regular",
            "fa-regular": "regular",
            fasl: "light",
            "fa-light": "light",
            fast: "thin",
            "fa-thin": "thin"
        },
        "sharp-duotone": {
            fa: "solid",
            fasds: "solid",
            "fa-solid": "solid"
        }
    }, y = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ], x = y.concat([ 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]), A = {
        GROUP: "duotone-group",
        SWAP_OPACITY: "swap-opacity",
        PRIMARY: "primary",
        SECONDARY: "secondary"
    }, N = [ ...Object.keys({
        classic: [ "fas", "far", "fal", "fat" ],
        sharp: [ "fass", "fasr", "fasl", "fast" ],
        "sharp-duotone": [ "fasds" ]
    }), "solid", "regular", "light", "thin", "duotone", "brands", "2xs", "xs", "sm", "lg", "xl", "2xl", "beat", "border", "fade", "beat-fade", "bounce", "flip-both", "flip-horizontal", "flip-vertical", "flip", "fw", "inverse", "layers-counter", "layers-text", "layers", "li", "pull-left", "pull-right", "pulse", "rotate-180", "rotate-270", "rotate-90", "rotate-by", "shake", "spin-pulse", "spin-reverse", "spin", "stack-1x", "stack-2x", "stack", "ul", A.GROUP, A.SWAP_OPACITY, A.PRIMARY, A.SECONDARY ].concat(y.map(t => "".concat(t, "x"))).concat(x.map(t => "w-".concat(t))), t = {
        kit: "fak"
    }, y = {
        "kit-duotone": "fakd"
    }, x = "___FONT_AWESOME___";
    const O = 16, P = "svg-inline--fa", C = "data-fa-i2svg", S = "data-fa-pseudo-element", E = "data-fa-pseudo-element-pending", M = "data-prefix", z = "data-icon", j = "fontawesome-i2svg", F = "async", L = [ "HTML", "HEAD", "STYLE", "SCRIPT" ], R = (() => {
        try {
            return !1;
        } catch (t) {
            return !1;
        }
    })(), I = [ l, d, p ];
    function D(t) {
        return new Proxy(t, {
            get(t, n) {
                return n in t ? t[n] : t[l];
            }
        });
    }
    const T = {
        ...v
    };
    T[l] = {
        ...v[l],
        ...g,
        ...b
    };
    const Y = D(T), H = {
        classic: {
            solid: "fas",
            regular: "far",
            light: "fal",
            thin: "fat",
            duotone: "fad",
            brands: "fab"
        },
        sharp: {
            solid: "fass",
            regular: "fasr",
            light: "fasl",
            thin: "fast"
        },
        "sharp-duotone": {
            solid: "fasds"
        }
    };
    H[l] = {
        ...H[l],
        ...t,
        ...y
    };
    const W = D(H), _ = {
        classic: {
            fab: "fa-brands",
            fad: "fa-duotone",
            fal: "fa-light",
            far: "fa-regular",
            fas: "fa-solid",
            fat: "fa-thin"
        },
        sharp: {
            fass: "fa-solid",
            fasr: "fa-regular",
            fasl: "fa-light",
            fast: "fa-thin"
        },
        "sharp-duotone": {
            fasds: "fa-solid"
        }
    };
    _[l] = {
        ..._[l],
        fak: "fa-kit"
    };
    const B = D(_), U = {
        classic: {
            "fa-brands": "fab",
            "fa-duotone": "fad",
            "fa-light": "fal",
            "fa-regular": "far",
            "fa-solid": "fas",
            "fa-thin": "fat"
        },
        sharp: {
            "fa-solid": "fass",
            "fa-regular": "fasr",
            "fa-light": "fasl",
            "fa-thin": "fast"
        },
        "sharp-duotone": {
            "fa-solid": "fasds"
        }
    };
    U[l] = {
        ...U[l],
        "fa-kit": "fak"
    };
    const X = D(U), q = /fa(s|r|l|t|d|b|k|kd|ss|sr|sl|st|sds)?[\-\ ]/, V = "fa-layers-text", G = /Font ?Awesome ?([56 ]*)(Solid|Regular|Light|Thin|Duotone|Brands|Free|Pro|Sharp Duotone|Sharp|Kit)?.*/i;
    D({
        classic: {
            900: "fas",
            400: "far",
            normal: "far",
            300: "fal",
            100: "fat"
        },
        sharp: {
            900: "fass",
            400: "fasr",
            300: "fasl",
            100: "fast"
        },
        "sharp-duotone": {
            900: "fasds"
        }
    });
    const K = [ "class", "data-prefix", "data-icon", "data-fa-transform", "data-fa-mask" ], J = A, Q = new Set();
    Object.keys(W[l]).map(Q.add.bind(Q)), Object.keys(W[d]).map(Q.add.bind(Q)), Object.keys(W[p]).map(Q.add.bind(Q));
    const Z = [ "kit", ...N ], $ = k.FontAwesomeConfig || {};
    if (w && "function" == typeof w.querySelector) {
        const Gn = [ [ "data-family-prefix", "familyPrefix" ], [ "data-css-prefix", "cssPrefix" ], [ "data-family-default", "familyDefault" ], [ "data-style-default", "styleDefault" ], [ "data-replacement-class", "replacementClass" ], [ "data-auto-replace-svg", "autoReplaceSvg" ], [ "data-auto-add-css", "autoAddCss" ], [ "data-auto-a11y", "autoA11y" ], [ "data-search-pseudo-elements", "searchPseudoElements" ], [ "data-observe-mutations", "observeMutations" ], [ "data-mutate-approach", "mutateApproach" ], [ "data-keep-original-source", "keepOriginalSource" ], [ "data-measure-performance", "measurePerformance" ], [ "data-show-missing-icons", "showMissingIcons" ] ];
        Gn.forEach(t => {
            var [ n, t ] = t, n = "" === (n = function(t) {
                var n = w.querySelector("script[" + t + "]");
                if (n) return n.getAttribute(t);
            }(n)) || "false" !== n && ("true" === n || n);
            null != n && ($[t] = n);
        });
    }
    y = {
        styleDefault: "solid",
        familyDefault: "classic",
        cssPrefix: "fa",
        replacementClass: P,
        autoReplaceSvg: !0,
        autoAddCss: !0,
        autoA11y: !0,
        searchPseudoElements: !1,
        observeMutations: !0,
        mutateApproach: "async",
        keepOriginalSource: !0,
        measurePerformance: !1,
        showMissingIcons: !0
    };
    $.familyPrefix && ($.cssPrefix = $.familyPrefix);
    const tt = {
        ...y,
        ...$
    };
    tt.autoReplaceSvg || (tt.observeMutations = !1);
    const nt = {};
    Object.keys(y).forEach(n => {
        Object.defineProperty(nt, n, {
            enumerable: !0,
            set: function(t) {
                tt[n] = t, et.forEach(t => t(nt));
            },
            get: function() {
                return tt[n];
            }
        });
    }), Object.defineProperty(nt, "familyPrefix", {
        enumerable: !0,
        set: function(t) {
            tt.cssPrefix = t, et.forEach(t => t(nt));
        },
        get: function() {
            return tt.cssPrefix;
        }
    }), k.FontAwesomeConfig = nt;
    const et = [];
    const at = O, rt = {
        size: 16,
        x: 0,
        y: 0,
        rotate: 0,
        flipX: !1,
        flipY: !1
    };
    const it = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    function ot() {
        let t = 12, n = "";
        for (;0 < t--; ) n += it[62 * Math.random() | 0];
        return n;
    }
    function st(n) {
        const e = [];
        for (let t = (n || []).length >>> 0; t--; ) e[t] = n[t];
        return e;
    }
    function ct(t) {
        return t.classList ? st(t.classList) : (t.getAttribute("class") || "").split(" ").filter(t => t);
    }
    function lt(t) {
        return "".concat(t).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&#39;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
    function ft(e) {
        return Object.keys(e || {}).reduce((t, n) => t + "".concat(n, ": ").concat(e[n].trim(), ";"), "");
    }
    function ut(t) {
        return t.size !== rt.size || t.x !== rt.x || t.y !== rt.y || t.rotate !== rt.rotate || t.flipX || t.flipY;
    }
    function mt() {
        var t, n, e = P, a = nt.cssPrefix, r = nt.replacementClass;
        let i = ':root, :host {\n  --fa-font-solid: normal 900 1em/1 "Font Awesome 6 Free";\n  --fa-font-regular: normal 400 1em/1 "Font Awesome 6 Free";\n  --fa-font-light: normal 300 1em/1 "Font Awesome 6 Pro";\n  --fa-font-thin: normal 100 1em/1 "Font Awesome 6 Pro";\n  --fa-font-duotone: normal 900 1em/1 "Font Awesome 6 Duotone";\n  --fa-font-brands: normal 400 1em/1 "Font Awesome 6 Brands";\n  --fa-font-sharp-solid: normal 900 1em/1 "Font Awesome 6 Sharp";\n  --fa-font-sharp-regular: normal 400 1em/1 "Font Awesome 6 Sharp";\n  --fa-font-sharp-light: normal 300 1em/1 "Font Awesome 6 Sharp";\n  --fa-font-sharp-thin: normal 100 1em/1 "Font Awesome 6 Sharp";\n  --fa-font-sharp-duotone-solid: normal 900 1em/1 "Font Awesome 6 Sharp Duotone";\n}\n\nsvg:not(:root).svg-inline--fa, svg:not(:host).svg-inline--fa {\n  overflow: visible;\n  box-sizing: content-box;\n}\n\n.svg-inline--fa {\n  display: var(--fa-display, inline-block);\n  height: 1em;\n  overflow: visible;\n  vertical-align: -0.125em;\n}\n.svg-inline--fa.fa-2xs {\n  vertical-align: 0.1em;\n}\n.svg-inline--fa.fa-xs {\n  vertical-align: 0em;\n}\n.svg-inline--fa.fa-sm {\n  vertical-align: -0.0714285705em;\n}\n.svg-inline--fa.fa-lg {\n  vertical-align: -0.2em;\n}\n.svg-inline--fa.fa-xl {\n  vertical-align: -0.25em;\n}\n.svg-inline--fa.fa-2xl {\n  vertical-align: -0.3125em;\n}\n.svg-inline--fa.fa-pull-left {\n  margin-right: var(--fa-pull-margin, 0.3em);\n  width: auto;\n}\n.svg-inline--fa.fa-pull-right {\n  margin-left: var(--fa-pull-margin, 0.3em);\n  width: auto;\n}\n.svg-inline--fa.fa-li {\n  width: var(--fa-li-width, 2em);\n  top: 0.25em;\n}\n.svg-inline--fa.fa-fw {\n  width: var(--fa-fw-width, 1.25em);\n}\n\n.fa-layers svg.svg-inline--fa {\n  bottom: 0;\n  left: 0;\n  margin: auto;\n  position: absolute;\n  right: 0;\n  top: 0;\n}\n\n.fa-layers-counter, .fa-layers-text {\n  display: inline-block;\n  position: absolute;\n  text-align: center;\n}\n\n.fa-layers {\n  display: inline-block;\n  height: 1em;\n  position: relative;\n  text-align: center;\n  vertical-align: -0.125em;\n  width: 1em;\n}\n.fa-layers svg.svg-inline--fa {\n  transform-origin: center center;\n}\n\n.fa-layers-text {\n  left: 50%;\n  top: 50%;\n  transform: translate(-50%, -50%);\n  transform-origin: center center;\n}\n\n.fa-layers-counter {\n  background-color: var(--fa-counter-background-color, #ff253a);\n  border-radius: var(--fa-counter-border-radius, 1em);\n  box-sizing: border-box;\n  color: var(--fa-inverse, #fff);\n  line-height: var(--fa-counter-line-height, 1);\n  max-width: var(--fa-counter-max-width, 5em);\n  min-width: var(--fa-counter-min-width, 1.5em);\n  overflow: hidden;\n  padding: var(--fa-counter-padding, 0.25em 0.5em);\n  right: var(--fa-right, 0);\n  text-overflow: ellipsis;\n  top: var(--fa-top, 0);\n  transform: scale(var(--fa-counter-scale, 0.25));\n  transform-origin: top right;\n}\n\n.fa-layers-bottom-right {\n  bottom: var(--fa-bottom, 0);\n  right: var(--fa-right, 0);\n  top: auto;\n  transform: scale(var(--fa-layers-scale, 0.25));\n  transform-origin: bottom right;\n}\n\n.fa-layers-bottom-left {\n  bottom: var(--fa-bottom, 0);\n  left: var(--fa-left, 0);\n  right: auto;\n  top: auto;\n  transform: scale(var(--fa-layers-scale, 0.25));\n  transform-origin: bottom left;\n}\n\n.fa-layers-top-right {\n  top: var(--fa-top, 0);\n  right: var(--fa-right, 0);\n  transform: scale(var(--fa-layers-scale, 0.25));\n  transform-origin: top right;\n}\n\n.fa-layers-top-left {\n  left: var(--fa-left, 0);\n  right: auto;\n  top: var(--fa-top, 0);\n  transform: scale(var(--fa-layers-scale, 0.25));\n  transform-origin: top left;\n}\n\n.fa-1x {\n  font-size: 1em;\n}\n\n.fa-2x {\n  font-size: 2em;\n}\n\n.fa-3x {\n  font-size: 3em;\n}\n\n.fa-4x {\n  font-size: 4em;\n}\n\n.fa-5x {\n  font-size: 5em;\n}\n\n.fa-6x {\n  font-size: 6em;\n}\n\n.fa-7x {\n  font-size: 7em;\n}\n\n.fa-8x {\n  font-size: 8em;\n}\n\n.fa-9x {\n  font-size: 9em;\n}\n\n.fa-10x {\n  font-size: 10em;\n}\n\n.fa-2xs {\n  font-size: 0.625em;\n  line-height: 0.1em;\n  vertical-align: 0.225em;\n}\n\n.fa-xs {\n  font-size: 0.75em;\n  line-height: 0.0833333337em;\n  vertical-align: 0.125em;\n}\n\n.fa-sm {\n  font-size: 0.875em;\n  line-height: 0.0714285718em;\n  vertical-align: 0.0535714295em;\n}\n\n.fa-lg {\n  font-size: 1.25em;\n  line-height: 0.05em;\n  vertical-align: -0.075em;\n}\n\n.fa-xl {\n  font-size: 1.5em;\n  line-height: 0.0416666682em;\n  vertical-align: -0.125em;\n}\n\n.fa-2xl {\n  font-size: 2em;\n  line-height: 0.03125em;\n  vertical-align: -0.1875em;\n}\n\n.fa-fw {\n  text-align: center;\n  width: 1.25em;\n}\n\n.fa-ul {\n  list-style-type: none;\n  margin-left: var(--fa-li-margin, 2.5em);\n  padding-left: 0;\n}\n.fa-ul > li {\n  position: relative;\n}\n\n.fa-li {\n  left: calc(-1 * var(--fa-li-width, 2em));\n  position: absolute;\n  text-align: center;\n  width: var(--fa-li-width, 2em);\n  line-height: inherit;\n}\n\n.fa-border {\n  border-color: var(--fa-border-color, #eee);\n  border-radius: var(--fa-border-radius, 0.1em);\n  border-style: var(--fa-border-style, solid);\n  border-width: var(--fa-border-width, 0.08em);\n  padding: var(--fa-border-padding, 0.2em 0.25em 0.15em);\n}\n\n.fa-pull-left {\n  float: left;\n  margin-right: var(--fa-pull-margin, 0.3em);\n}\n\n.fa-pull-right {\n  float: right;\n  margin-left: var(--fa-pull-margin, 0.3em);\n}\n\n.fa-beat {\n  animation-name: fa-beat;\n  animation-delay: var(--fa-animation-delay, 0s);\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 1s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, ease-in-out);\n}\n\n.fa-bounce {\n  animation-name: fa-bounce;\n  animation-delay: var(--fa-animation-delay, 0s);\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 1s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.28, 0.84, 0.42, 1));\n}\n\n.fa-fade {\n  animation-name: fa-fade;\n  animation-delay: var(--fa-animation-delay, 0s);\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 1s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));\n}\n\n.fa-beat-fade {\n  animation-name: fa-beat-fade;\n  animation-delay: var(--fa-animation-delay, 0s);\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 1s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));\n}\n\n.fa-flip {\n  animation-name: fa-flip;\n  animation-delay: var(--fa-animation-delay, 0s);\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 1s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, ease-in-out);\n}\n\n.fa-shake {\n  animation-name: fa-shake;\n  animation-delay: var(--fa-animation-delay, 0s);\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 1s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, linear);\n}\n\n.fa-spin {\n  animation-name: fa-spin;\n  animation-delay: var(--fa-animation-delay, 0s);\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 2s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, linear);\n}\n\n.fa-spin-reverse {\n  --fa-animation-direction: reverse;\n}\n\n.fa-pulse,\n.fa-spin-pulse {\n  animation-name: fa-spin;\n  animation-direction: var(--fa-animation-direction, normal);\n  animation-duration: var(--fa-animation-duration, 1s);\n  animation-iteration-count: var(--fa-animation-iteration-count, infinite);\n  animation-timing-function: var(--fa-animation-timing, steps(8));\n}\n\n@media (prefers-reduced-motion: reduce) {\n  .fa-beat,\n.fa-bounce,\n.fa-fade,\n.fa-beat-fade,\n.fa-flip,\n.fa-pulse,\n.fa-shake,\n.fa-spin,\n.fa-spin-pulse {\n    animation-delay: -1ms;\n    animation-duration: 1ms;\n    animation-iteration-count: 1;\n    transition-delay: 0s;\n    transition-duration: 0s;\n  }\n}\n@keyframes fa-beat {\n  0%, 90% {\n    transform: scale(1);\n  }\n  45% {\n    transform: scale(var(--fa-beat-scale, 1.25));\n  }\n}\n@keyframes fa-bounce {\n  0% {\n    transform: scale(1, 1) translateY(0);\n  }\n  10% {\n    transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);\n  }\n  30% {\n    transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));\n  }\n  50% {\n    transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);\n  }\n  57% {\n    transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));\n  }\n  64% {\n    transform: scale(1, 1) translateY(0);\n  }\n  100% {\n    transform: scale(1, 1) translateY(0);\n  }\n}\n@keyframes fa-fade {\n  50% {\n    opacity: var(--fa-fade-opacity, 0.4);\n  }\n}\n@keyframes fa-beat-fade {\n  0%, 100% {\n    opacity: var(--fa-beat-fade-opacity, 0.4);\n    transform: scale(1);\n  }\n  50% {\n    opacity: 1;\n    transform: scale(var(--fa-beat-fade-scale, 1.125));\n  }\n}\n@keyframes fa-flip {\n  50% {\n    transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));\n  }\n}\n@keyframes fa-shake {\n  0% {\n    transform: rotate(-15deg);\n  }\n  4% {\n    transform: rotate(15deg);\n  }\n  8%, 24% {\n    transform: rotate(-18deg);\n  }\n  12%, 28% {\n    transform: rotate(18deg);\n  }\n  16% {\n    transform: rotate(-22deg);\n  }\n  20% {\n    transform: rotate(22deg);\n  }\n  32% {\n    transform: rotate(-12deg);\n  }\n  36% {\n    transform: rotate(12deg);\n  }\n  40%, 100% {\n    transform: rotate(0deg);\n  }\n}\n@keyframes fa-spin {\n  0% {\n    transform: rotate(0deg);\n  }\n  100% {\n    transform: rotate(360deg);\n  }\n}\n.fa-rotate-90 {\n  transform: rotate(90deg);\n}\n\n.fa-rotate-180 {\n  transform: rotate(180deg);\n}\n\n.fa-rotate-270 {\n  transform: rotate(270deg);\n}\n\n.fa-flip-horizontal {\n  transform: scale(-1, 1);\n}\n\n.fa-flip-vertical {\n  transform: scale(1, -1);\n}\n\n.fa-flip-both,\n.fa-flip-horizontal.fa-flip-vertical {\n  transform: scale(-1, -1);\n}\n\n.fa-rotate-by {\n  transform: rotate(var(--fa-rotate-angle, 0));\n}\n\n.fa-stack {\n  display: inline-block;\n  vertical-align: middle;\n  height: 2em;\n  position: relative;\n  width: 2.5em;\n}\n\n.fa-stack-1x,\n.fa-stack-2x {\n  bottom: 0;\n  left: 0;\n  margin: auto;\n  position: absolute;\n  right: 0;\n  top: 0;\n  z-index: var(--fa-stack-z-index, auto);\n}\n\n.svg-inline--fa.fa-stack-1x {\n  height: 1em;\n  width: 1.25em;\n}\n.svg-inline--fa.fa-stack-2x {\n  height: 2em;\n  width: 2.5em;\n}\n\n.fa-inverse {\n  color: var(--fa-inverse, #fff);\n}\n\n.sr-only,\n.fa-sr-only {\n  position: absolute;\n  width: 1px;\n  height: 1px;\n  padding: 0;\n  margin: -1px;\n  overflow: hidden;\n  clip: rect(0, 0, 0, 0);\n  white-space: nowrap;\n  border-width: 0;\n}\n\n.sr-only-focusable:not(:focus),\n.fa-sr-only-focusable:not(:focus) {\n  position: absolute;\n  width: 1px;\n  height: 1px;\n  padding: 0;\n  margin: -1px;\n  overflow: hidden;\n  clip: rect(0, 0, 0, 0);\n  white-space: nowrap;\n  border-width: 0;\n}\n\n.svg-inline--fa .fa-primary {\n  fill: var(--fa-primary-color, currentColor);\n  opacity: var(--fa-primary-opacity, 1);\n}\n\n.svg-inline--fa .fa-secondary {\n  fill: var(--fa-secondary-color, currentColor);\n  opacity: var(--fa-secondary-opacity, 0.4);\n}\n\n.svg-inline--fa.fa-swap-opacity .fa-primary {\n  opacity: var(--fa-secondary-opacity, 0.4);\n}\n\n.svg-inline--fa.fa-swap-opacity .fa-secondary {\n  opacity: var(--fa-primary-opacity, 1);\n}\n\n.svg-inline--fa mask .fa-primary,\n.svg-inline--fa mask .fa-secondary {\n  fill: black;\n}\n\n.fad.fa-inverse,\n.fa-duotone.fa-inverse {\n  color: var(--fa-inverse, #fff);\n}';
        return "fa" === a && r === e || (t = new RegExp("\\.".concat("fa", "\\-"), "g"), 
        n = new RegExp("\\--".concat("fa", "\\-"), "g"), e = new RegExp("\\.".concat(e), "g"), 
        i = i.replace(t, ".".concat(a, "-")).replace(n, "--".concat(a, "-")).replace(e, ".".concat(r))), 
        i;
    }
    let dt = !1;
    function pt() {
        nt.autoAddCss && !dt && (function(t) {
            if (t && f) {
                const r = w.createElement("style");
                r.setAttribute("type", "text/css"), r.innerHTML = t;
                var e = w.head.childNodes;
                let n = null;
                for (let t = e.length - 1; -1 < t; t--) {
                    const i = e[t];
                    var a = (i.tagName || "").toUpperCase();
                    -1 < [ "STYLE", "LINK" ].indexOf(a) && (n = i);
                }
                w.head.insertBefore(r, n);
            }
        }(mt()), dt = !0);
    }
    A = {
        mixout() {
            return {
                dom: {
                    css: mt,
                    insertCss: pt
                }
            };
        },
        hooks() {
            return {
                beforeDOMElementCreation() {
                    pt();
                },
                beforeI2svg() {
                    pt();
                }
            };
        }
    };
    const ht = k || {};
    ht[x] || (ht[x] = {}), ht[x].styles || (ht[x].styles = {}), ht[x].hooks || (ht[x].hooks = {}), 
    ht[x].shims || (ht[x].shims = []);
    var gt = ht[x];
    function bt() {
        w.removeEventListener("DOMContentLoaded", bt), yt = 1, vt.map(t => t());
    }
    const vt = [];
    let yt = !1;
    function xt(t) {
        f && (yt ? setTimeout(t, 0) : vt.push(t));
    }
    function kt(t) {
        const {
            tag: n,
            attributes: e = {},
            children: a = []
        } = t;
        return "string" == typeof t ? lt(t) : "<".concat(n, " ").concat((r = e, Object.keys(r || {}).reduce((t, n) => t + "".concat(n, '="').concat(lt(r[n]), '" '), "").trim()), ">").concat(a.map(kt).join(""), "</").concat(n, ">");
        var r;
    }
    function wt(t, n, e) {
        if (t && t[n] && t[n][e]) return {
            prefix: n,
            iconName: e,
            icon: t[n][e]
        };
    }
    f && (yt = (w.documentElement.doScroll ? /^loaded|^c/ : /^loaded|^i|^c/).test(w.readyState), 
    yt || w.addEventListener("DOMContentLoaded", bt));
    function At(t, n, e, a) {
        for (var r, i, o = Object.keys(t), s = o.length, c = void 0 !== a ? Nt(n, a) : n, l = void 0 === e ? (r = 1, 
        t[o[0]]) : (r = 0, e); r < s; r++) l = c(l, t[i = o[r]], i, t);
        return l;
    }
    var Nt = function(r, i) {
        return function(t, n, e, a) {
            return r.call(i, t, n, e, a);
        };
    };
    function Ot(t) {
        const n = function(t) {
            const n = [];
            let e = 0;
            for (var a = t.length; e < a; ) {
                var r, i = t.charCodeAt(e++);
                55296 <= i && i <= 56319 && e < a ? 56320 == (64512 & (r = t.charCodeAt(e++))) ? n.push(((1023 & i) << 10) + (1023 & r) + 65536) : (n.push(i), 
                e--) : n.push(i);
            }
            return n;
        }(t);
        return 1 === n.length ? n[0].toString(16) : null;
    }
    function Pt(a) {
        return Object.keys(a).reduce((t, n) => {
            var e = a[n];
            return !!e.icon ? t[e.iconName] = e.icon : t[n] = e, t;
        }, {});
    }
    function Ct(t, n, e) {
        var {
            skipHooks: a = !1
        } = 2 < arguments.length && void 0 !== e ? e : {}, e = Pt(n);
        "function" != typeof gt.hooks.addPack || a ? gt.styles[t] = {
            ...gt.styles[t] || {},
            ...e
        } : gt.hooks.addPack(t, Pt(n)), "fas" === t && Ct("fa", n);
    }
    const {
        styles: St,
        shims: Et
    } = gt, Mt = {
        classic: Object.values(B[l]),
        sharp: Object.values(B[d]),
        "sharp-duotone": Object.values(B[p])
    };
    let zt = null, jt = {}, Ft = {}, Lt = {}, Rt = {}, It = {};
    const Dt = {
        classic: Object.keys(Y[l]),
        sharp: Object.keys(Y[d]),
        "sharp-duotone": Object.keys(Y[p])
    };
    function Tt(t, n) {
        const e = n.split("-");
        var a = e[0], n = e.slice(1).join("-");
        return a !== t || "" === n || (t = n, ~Z.indexOf(t)) ? null : n;
    }
    const Yt = () => {
        var t = a => At(St, (t, n, e) => (t[e] = At(n, a, {}), t), {});
        jt = t((n, t, e) => {
            if (t[3] && (n[t[3]] = e), t[2]) {
                const a = t[2].filter(t => "number" == typeof t);
                a.forEach(t => {
                    n[t.toString(16)] = e;
                });
            }
            return n;
        }), Ft = t((n, t, e) => {
            if (n[e] = e, t[2]) {
                const a = t[2].filter(t => "string" == typeof t);
                a.forEach(t => {
                    n[t] = e;
                });
            }
            return n;
        }), It = t((n, t, e) => {
            const a = t[2];
            return n[e] = e, a.forEach(t => {
                n[t] = e;
            }), n;
        });
        const r = "far" in St || nt.autoFetchSvg;
        t = At(Et, (t, n) => {
            const e = n[0];
            let a = n[1];
            n = n[2];
            return "far" !== a || r || (a = "fas"), "string" == typeof e && (t.names[e] = {
                prefix: a,
                iconName: n
            }), "number" == typeof e && (t.unicodes[e.toString(16)] = {
                prefix: a,
                iconName: n
            }), t;
        }, {
            names: {},
            unicodes: {}
        });
        Lt = t.names, Rt = t.unicodes, zt = Ut(nt.styleDefault, {
            family: nt.familyDefault
        });
    };
    function Ht(t, n) {
        return (jt[t] || {})[n];
    }
    function Wt(t, n) {
        return (It[t] || {})[n];
    }
    function _t(t) {
        return Lt[t] || {
            prefix: null,
            iconName: null
        };
    }
    N = t => {
        zt = Ut(t.styleDefault, {
            family: nt.familyDefault
        });
    }, et.push(N), Yt();
    const Bt = () => ({
        prefix: null,
        iconName: null,
        rest: []
    });
    function Ut(t, n) {
        var {
            family: e = l
        } = 1 < arguments.length && void 0 !== n ? n : {}, n = Y[e][t], n = W[e][t] || W[e][n], t = t in gt.styles ? t : null;
        return n || t || null;
    }
    const Xt = {
        classic: Object.keys(B[l]),
        sharp: Object.keys(B[d]),
        "sharp-duotone": Object.keys(B[p])
    };
    function qt(t, n) {
        const {
            skipLookups: r = !1
        } = 1 < arguments.length && void 0 !== n ? n : {}, i = {
            classic: "".concat(nt.cssPrefix, "-").concat(l),
            sharp: "".concat(nt.cssPrefix, "-").concat(d),
            "sharp-duotone": "".concat(nt.cssPrefix, "-").concat(p)
        };
        let o = null, s = l;
        const c = h.filter(t => t !== m);
        c.forEach(n => {
            (t.includes(i[n]) || t.some(t => Xt[n].includes(t))) && (s = n);
        });
        const e = t.reduce((t, n) => {
            var e, a = Tt(nt.cssPrefix, n);
            return St[n] ? (n = Mt[s].includes(n) ? X[s][n] : n, o = n, t.prefix = n) : -1 < Dt[s].indexOf(n) ? (o = n, 
            t.prefix = Ut(n, {
                family: s
            })) : a ? t.iconName = a : n === nt.replacementClass || c.some(t => n === i[t]) || t.rest.push(n), 
            !r && t.prefix && t.iconName && (e = "fa" === o ? _t(t.iconName) : {}, a = Wt(t.prefix, t.iconName), 
            e.prefix && (o = null), t.iconName = e.iconName || a || t.iconName, t.prefix = e.prefix || t.prefix, 
            "far" !== t.prefix || St.far || !St.fas || nt.autoFetchSvg || (t.prefix = "fas")), 
            t;
        }, Bt());
        return (t.includes("fa-brands") || t.includes("fab")) && (e.prefix = "fab"), (t.includes("fa-duotone") || t.includes("fad")) && (e.prefix = "fad"), 
        e.prefix || s !== d || !St.fass && !nt.autoFetchSvg || (e.prefix = "fass", e.iconName = Wt(e.prefix, e.iconName) || e.iconName), 
        e.prefix || s !== p || !St.fasds && !nt.autoFetchSvg || (e.prefix = "fasds", e.iconName = Wt(e.prefix, e.iconName) || e.iconName), 
        "fa" !== e.prefix && "fa" !== o || (e.prefix = zt || "fas"), e;
    }
    let Vt = [], Gt = {};
    const Kt = {}, Jt = Object.keys(Kt);
    function Qt(t, n) {
        for (var e = arguments.length, a = new Array(2 < e ? e - 2 : 0), r = 2; r < e; r++) a[r - 2] = arguments[r];
        const i = Gt[t] || [];
        return i.forEach(t => {
            n = t.apply(null, [ n, ...a ]);
        }), n;
    }
    function Zt(t) {
        for (var n = arguments.length, e = new Array(1 < n ? n - 1 : 0), a = 1; a < n; a++) e[a - 1] = arguments[a];
        const r = Gt[t] || [];
        r.forEach(t => {
            t.apply(null, e);
        });
    }
    function $t(t) {
        var n = t, t = Array.prototype.slice.call(arguments, 1);
        return Kt[n] ? Kt[n].apply(null, t) : void 0;
    }
    function tn(t) {
        "fa" === t.prefix && (t.prefix = "fas");
        let n = t["iconName"];
        t = t.prefix || zt;
        if (n) return n = Wt(t, n) || n, wt(nn.definitions, t, n) || wt(gt.styles, t, n);
    }
    const nn = new class {
        constructor() {
            this.definitions = {};
        }
        add() {
            for (var t = arguments.length, n = new Array(t), e = 0; e < t; e++) n[e] = arguments[e];
            const a = n.reduce(this._pullDefinitions, {});
            Object.keys(a).forEach(t => {
                this.definitions[t] = {
                    ...this.definitions[t] || {},
                    ...a[t]
                }, Ct(t, a[t]);
                var n = B[l][t];
                n && Ct(n, a[t]), Yt();
            });
        }
        reset() {
            this.definitions = {};
        }
        _pullDefinitions(i, t) {
            const o = t.prefix && t.iconName && t.icon ? {
                0: t
            } : t;
            return Object.keys(o).map(t => {
                const {
                    prefix: n,
                    iconName: e,
                    icon: a
                } = o[t], r = a[2];
                i[n] || (i[n] = {}), 0 < r.length && r.forEach(t => {
                    "string" == typeof t && (i[n][t] = a);
                }), i[n][e] = a;
            }), i;
        }
    }();
    const en = {
        noAuto: () => {
            nt.autoReplaceSvg = !1, nt.observeMutations = !1, Zt("noAuto");
        },
        config: nt,
        dom: {
            i2svg: function() {
                var t = 0 < arguments.length && void 0 !== arguments[0] ? arguments[0] : {};
                return f ? (Zt("beforeI2svg", t), $t("pseudoElements2svg", t), $t("i2svg", t)) : Promise.reject(new Error("Operation requires a DOM of some kind."));
            },
            watch: function() {
                let t = 0 < arguments.length && void 0 !== arguments[0] ? arguments[0] : {};
                const n = t["autoReplaceSvgRoot"];
                !1 === nt.autoReplaceSvg && (nt.autoReplaceSvg = !0), nt.observeMutations = !0, 
                xt(() => {
                    an({
                        autoReplaceSvgRoot: n
                    }), Zt("watch", t);
                });
            }
        },
        parse: {
            icon: t => {
                if (null === t) return null;
                if ("object" == typeof t && t.prefix && t.iconName) return {
                    prefix: t.prefix,
                    iconName: Wt(t.prefix, t.iconName) || t.iconName
                };
                if (Array.isArray(t) && 2 === t.length) {
                    var n = 0 === t[1].indexOf("fa-") ? t[1].slice(3) : t[1], e = Ut(t[0]);
                    return {
                        prefix: e,
                        iconName: Wt(e, n) || n
                    };
                }
                if ("string" == typeof t && (-1 < t.indexOf("".concat(nt.cssPrefix, "-")) || t.match(q))) {
                    n = qt(t.split(" "), {
                        skipLookups: !0
                    });
                    return {
                        prefix: n.prefix || zt,
                        iconName: Wt(n.prefix, n.iconName) || n.iconName
                    };
                }
                return "string" == typeof t ? {
                    prefix: zt,
                    iconName: Wt(zt, t) || t
                } : void 0;
            }
        },
        library: nn,
        findIconDefinition: tn,
        toHtml: kt
    }, an = function() {
        var t = 0 < arguments.length && void 0 !== arguments[0] ? arguments[0] : {}, {
            autoReplaceSvgRoot: t = w
        } = t;
        (0 < Object.keys(gt.styles).length || nt.autoFetchSvg) && f && nt.autoReplaceSvg && en.dom.i2svg({
            node: t
        });
    };
    function rn(n, t) {
        return Object.defineProperty(n, "abstract", {
            get: t
        }), Object.defineProperty(n, "html", {
            get: function() {
                return n.abstract.map(t => kt(t));
            }
        }), Object.defineProperty(n, "node", {
            get: function() {
                if (f) {
                    const t = w.createElement("div");
                    return t.innerHTML = n.html, t.children;
                }
            }
        }), n;
    }
    function on(t) {
        const {
            icons: {
                main: n,
                mask: e
            },
            prefix: a,
            iconName: r,
            transform: i,
            symbol: o,
            title: s,
            maskId: c,
            titleId: l,
            extra: f,
            watchable: u = !1
        } = t;
        var {
            width: m,
            height: d
        } = e.found ? e : n, p = "fak" === a, t = [ nt.replacementClass, r ? "".concat(nt.cssPrefix, "-").concat(r) : "" ].filter(t => -1 === f.classes.indexOf(t)).filter(t => "" !== t || !!t).concat(f.classes).join(" ");
        let h = {
            children: [],
            attributes: {
                ...f.attributes,
                "data-prefix": a,
                "data-icon": r,
                class: t,
                role: f.attributes.role || "img",
                xmlns: "http://www.w3.org/2000/svg",
                viewBox: "0 0 ".concat(m, " ").concat(d)
            }
        };
        m = p && !~f.classes.indexOf("fa-fw") ? {
            width: "".concat(m / d * 16 * .0625, "em")
        } : {};
        u && (h.attributes[C] = ""), s && (h.children.push({
            tag: "title",
            attributes: {
                id: h.attributes["aria-labelledby"] || "title-".concat(l || ot())
            },
            children: [ s ]
        }), delete h.attributes.title);
        const g = {
            ...h,
            prefix: a,
            iconName: r,
            main: n,
            mask: e,
            maskId: c,
            transform: i,
            symbol: o,
            styles: {
                ...m,
                ...f.styles
            }
        };
        var {
            children: d,
            attributes: m
        } = e.found && n.found ? $t("generateAbstractMask", g) || {
            children: [],
            attributes: {}
        } : $t("generateAbstractIcon", g) || {
            children: [],
            attributes: {}
        };
        return g.children = d, g.attributes = m, (o ? function(t) {
            var {
                prefix: n,
                iconName: e,
                children: a,
                attributes: r,
                symbol: t
            } = t, t = !0 === t ? "".concat(n, "-").concat(nt.cssPrefix, "-").concat(e) : t;
            return [ {
                tag: "svg",
                attributes: {
                    style: "display: none;"
                },
                children: [ {
                    tag: "symbol",
                    attributes: {
                        ...r,
                        id: t
                    },
                    children: a
                } ]
            } ];
        } : function(t) {
            let {
                children: n,
                main: e,
                mask: a,
                attributes: r,
                styles: i,
                transform: o
            } = t;
            if (ut(o) && e.found && !a.found) {
                var {
                    width: s,
                    height: t
                } = e;
                const c = s / t / 2, l = .5;
                r.style = ft({
                    ...i,
                    "transform-origin": "".concat(c + o.x / 16, "em ").concat(l + o.y / 16, "em")
                });
            }
            return [ {
                tag: "svg",
                attributes: r,
                children: n
            } ];
        })(g);
    }
    function sn(t) {
        const {
            content: n,
            width: e,
            height: a,
            transform: r,
            title: i,
            extra: o,
            watchable: s = !1
        } = t, c = {
            ...o.attributes,
            ...i ? {
                title: i
            } : {},
            class: o.classes.join(" ")
        };
        s && (c[C] = "");
        const l = {
            ...o.styles
        };
        ut(r) && (l.transform = function(t) {
            var {
                transform: n,
                width: e = O,
                height: a = O,
                startCentered: t = !1
            } = t;
            let r = "";
            return t && u ? r += "translate(".concat(n.x / at - e / 2, "em, ").concat(n.y / at - a / 2, "em) ") : r += t ? "translate(calc(-50% + ".concat(n.x / at, "em), calc(-50% + ").concat(n.y / at, "em)) ") : "translate(".concat(n.x / at, "em, ").concat(n.y / at, "em) "), 
            r += "scale(".concat(n.size / at * (n.flipX ? -1 : 1), ", ").concat(n.size / at * (n.flipY ? -1 : 1), ") "), 
            r += "rotate(".concat(n.rotate, "deg) "), r;
        }({
            transform: r,
            startCentered: !0,
            width: e,
            height: a
        }), l["-webkit-transform"] = l.transform);
        t = ft(l);
        0 < t.length && (c.style = t);
        const f = [];
        return f.push({
            tag: "span",
            attributes: c,
            children: [ n ]
        }), i && f.push({
            tag: "span",
            attributes: {
                class: "sr-only"
            },
            children: [ i ]
        }), f;
    }
    const cn = gt["styles"];
    function ln(t) {
        var n = t[0], e = t[1], [ t ] = t.slice(4);
        let a = null;
        return a = Array.isArray(t) ? {
            tag: "g",
            attributes: {
                class: "".concat(nt.cssPrefix, "-").concat(J.GROUP)
            },
            children: [ {
                tag: "path",
                attributes: {
                    class: "".concat(nt.cssPrefix, "-").concat(J.SECONDARY),
                    fill: "currentColor",
                    d: t[0]
                }
            }, {
                tag: "path",
                attributes: {
                    class: "".concat(nt.cssPrefix, "-").concat(J.PRIMARY),
                    fill: "currentColor",
                    d: t[1]
                }
            } ]
        } : {
            tag: "path",
            attributes: {
                fill: "currentColor",
                d: t
            }
        }, {
            found: !0,
            width: n,
            height: e,
            icon: a
        };
    }
    const fn = {
        found: !1,
        width: 512,
        height: 512
    };
    function un(r, i) {
        let o = i;
        return "fa" === i && null !== nt.styleDefault && (i = zt), new Promise((t, n) => {
            var e, a;
            if ("fa" === o && (a = _t(r) || {}, r = a.iconName || r, i = a.prefix || i), r && i && cn[i] && cn[i][r]) return t(ln(cn[i][r]));
            e = r, a = i, R || nt.showMissingIcons || !e || console.error('Icon with name "'.concat(e, '" and prefix "').concat(a, '" is missing.')), 
            t({
                ...fn,
                icon: nt.showMissingIcons && r && $t("missingIconAbstract") || {}
            });
        });
    }
    y = () => {};
    const mn = nt.measurePerformance && o && o.mark && o.measure ? o : {
        mark: y,
        measure: y
    }, dn = 'FA "6.6.0"';
    const pn = t => {
        mn.mark("".concat(dn, " ").concat(t, " ends")), mn.measure("".concat(dn, " ").concat(t), "".concat(dn, " ").concat(t, " begins"), "".concat(dn, " ").concat(t, " ends"));
    };
    var hn = {
        begin: t => (mn.mark("".concat(dn, " ").concat(t, " begins")), () => pn(t)),
        end: pn
    };
    const gn = () => {};
    function bn(t) {
        return "string" == typeof (t.getAttribute ? t.getAttribute(C) : null);
    }
    function vn(n, t) {
        const {
            ceFn: e = "svg" === n.tag ? function(t) {
                return w.createElementNS("http://www.w3.org/2000/svg", t);
            } : function(t) {
                return w.createElement(t);
            }
        } = 1 < arguments.length && void 0 !== t ? t : {};
        if ("string" == typeof n) return w.createTextNode(n);
        const a = e(n.tag);
        Object.keys(n.attributes || []).forEach(function(t) {
            a.setAttribute(t, n.attributes[t]);
        });
        const r = n.children || [];
        return r.forEach(function(t) {
            a.appendChild(vn(t, {
                ceFn: e
            }));
        }), a;
    }
    const yn = {
        replace: function(t) {
            const n = t[0];
            n.parentNode && (t[1].forEach(t => {
                n.parentNode.insertBefore(vn(t), n);
            }), null === n.getAttribute(C) && nt.keepOriginalSource ? (t = w.createComment((t = n, 
            t = " ".concat(t.outerHTML, " "), t = "".concat(t, "Font Awesome fontawesome.com "))), 
            n.parentNode.replaceChild(t, n)) : n.remove());
        },
        nest: function(t) {
            const n = t[0], e = t[1];
            if (~ct(n).indexOf(nt.replacementClass)) return yn.replace(t);
            const a = new RegExp("".concat(nt.cssPrefix, "-.*"));
            if (delete e[0].attributes.id, e[0].attributes.class) {
                const r = e[0].attributes.class.split(" ").reduce((t, n) => ((n === nt.replacementClass || n.match(a) ? t.toSvg : t.toNode).push(n), 
                t), {
                    toNode: [],
                    toSvg: []
                });
                e[0].attributes.class = r.toSvg.join(" "), 0 === r.toNode.length ? n.removeAttribute("class") : n.setAttribute("class", r.toNode.join(" "));
            }
            t = e.map(t => kt(t)).join("\n");
            n.setAttribute(C, ""), n.innerHTML = t;
        }
    };
    function xn(t) {
        t();
    }
    function kn(e, t) {
        const a = "function" == typeof t ? t : gn;
        if (0 === e.length) a(); else {
            let t = xn;
            nt.mutateApproach === F && (t = k.requestAnimationFrame || xn), t(() => {
                var t = !0 !== nt.autoReplaceSvg && yn[nt.autoReplaceSvg] || yn.replace;
                const n = hn.begin("mutate");
                e.map(t), n(), a();
            });
        }
    }
    let wn = !1;
    function An() {
        wn = !0;
    }
    function Nn() {
        wn = !1;
    }
    let On = null;
    function Pn(t) {
        if (!c) return;
        if (!nt.observeMutations) return;
        const {
            treeCallback: i = gn,
            nodeCallback: o = gn,
            pseudoElementsCallback: s = gn,
            observeMutationsRoot: n = w
        } = t;
        On = new c(t => {
            if (!wn) {
                const r = zt;
                st(t).forEach(t => {
                    var n, e, a;
                    "childList" === t.type && 0 < t.addedNodes.length && !bn(t.addedNodes[0]) && (nt.searchPseudoElements && s(t.target), 
                    i(t.target)), "attributes" === t.type && t.target.parentNode && nt.searchPseudoElements && s(t.target.parentNode), 
                    "attributes" === t.type && bn(t.target) && ~K.indexOf(t.attributeName) && ("class" === t.attributeName && (e = t.target, 
                    a = e.getAttribute ? e.getAttribute(M) : null, e = e.getAttribute ? e.getAttribute(z) : null, 
                    a && e) ? ({
                        prefix: e,
                        iconName: n
                    } = qt(ct(t.target)), t.target.setAttribute(M, e || r), n && t.target.setAttribute(z, n)) : (n = t.target) && n.classList && n.classList.contains && n.classList.contains(nt.replacementClass) && o(t.target));
                });
            }
        }), f && On.observe(n, {
            childList: !0,
            attributes: !0,
            characterData: !0,
            subtree: !0
        });
    }
    function Cn(t) {
        var n = t.getAttribute("data-prefix"), e = t.getAttribute("data-icon"), a = void 0 !== t.innerText ? t.innerText.trim() : "";
        let r = qt(ct(t));
        return r.prefix || (r.prefix = zt), n && e && (r.prefix = n, r.iconName = e), r.iconName && r.prefix || (r.prefix && 0 < a.length && (r.iconName = (e = r.prefix, 
        a = t.innerText, (Ft[e] || {})[a] || Ht(r.prefix, Ot(t.innerText)))), !r.iconName && nt.autoFetchSvg && t.firstChild && t.firstChild.nodeType === Node.TEXT_NODE && (r.iconName = t.firstChild.data)), 
        r;
    }
    function Sn(t, n) {
        var e = 1 < arguments.length && void 0 !== n ? n : {
            styleParser: !0
        }, {
            iconName: a,
            prefix: r,
            rest: i
        } = Cn(t), o = function(t) {
            const n = st(t.attributes).reduce((t, n) => ("class" !== t.name && "style" !== t.name && (t[n.name] = n.value), 
            t), {});
            var e = t.getAttribute("title"), t = t.getAttribute("data-fa-title-id");
            return nt.autoA11y && (e ? n["aria-labelledby"] = "".concat(nt.replacementClass, "-title-").concat(t || ot()) : (n["aria-hidden"] = "true", 
            n.focusable = "false")), n;
        }(t), n = Qt("parseNodeAttributes", {}, t), e = e.styleParser ? function(t) {
            const n = t.getAttribute("style");
            let e = [];
            return n && (e = n.split(";").reduce((t, n) => {
                const e = n.split(":");
                n = e[0];
                const a = e.slice(1);
                return n && 0 < a.length && (t[n] = a.join(":").trim()), t;
            }, {})), e;
        }(t) : [];
        return {
            iconName: a,
            title: t.getAttribute("title"),
            titleId: t.getAttribute("data-fa-title-id"),
            prefix: r,
            transform: rt,
            mask: {
                iconName: null,
                prefix: null,
                rest: []
            },
            maskId: null,
            symbol: !1,
            extra: {
                classes: i,
                styles: e,
                attributes: o
            },
            ...n
        };
    }
    const En = gt["styles"];
    function Mn(t) {
        const n = "nest" === nt.autoReplaceSvg ? Sn(t, {
            styleParser: !1
        }) : Sn(t);
        return ~n.extra.classes.indexOf(V) ? $t("generateLayersText", t, n) : $t("generateSvgReplacementMutation", t, n);
    }
    let zn = new Set();
    function jn(t) {
        let a = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : null;
        if (!f) return Promise.resolve();
        const n = w.documentElement.classList, r = t => n.add("".concat(j, "-").concat(t)), i = t => n.remove("".concat(j, "-").concat(t)), e = nt.autoFetchSvg ? zn : I.map(t => "fa-".concat(t)).concat(Object.keys(En));
        e.includes("fa") || e.push("fa");
        var o = [ ".".concat(V, ":not([").concat(C, "])") ].concat(e.map(t => ".".concat(t, ":not([").concat(C, "])"))).join(", ");
        if (0 === o.length) return Promise.resolve();
        let s = [];
        try {
            s = st(t.querySelectorAll(o));
        } catch (t) {}
        if (!(0 < s.length)) return Promise.resolve();
        r("pending"), i("complete");
        const c = hn.begin("onTree"), l = s.reduce((t, n) => {
            try {
                var e = Mn(n);
                e && t.push(e);
            } catch (t) {
                R || "MissingIcon" === t.name && console.error(t);
            }
            return t;
        }, []);
        return new Promise((n, e) => {
            Promise.all(l).then(t => {
                kn(t, () => {
                    r("active"), r("complete"), i("pending"), "function" == typeof a && a(), c(), n();
                });
            }).catch(t => {
                c(), e(t);
            });
        });
    }
    function Fn(t) {
        let n = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : null;
        Mn(t).then(t => {
            t && kn([ t ], n);
        });
    }
    I.map(t => {
        zn.add("fa-".concat(t));
    }), Object.keys(Y[l]).map(zn.add.bind(zn)), Object.keys(Y[d]).map(zn.add.bind(zn)), 
    Object.keys(Y[p]).map(zn.add.bind(zn)), zn = [ ...zn ];
    function Ln(t) {
        let n = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
        const {
            transform: e = rt,
            symbol: a = !1,
            mask: r = null,
            maskId: i = null,
            title: o = null,
            titleId: s = null,
            classes: c = [],
            attributes: l = {},
            styles: f = {}
        } = n;
        if (t) {
            const {
                prefix: u,
                iconName: m,
                icon: d
            } = t;
            return rn({
                type: "icon",
                ...t
            }, () => (Zt("beforeDOMElementCreation", {
                iconDefinition: t,
                params: n
            }), nt.autoA11y && (o ? l["aria-labelledby"] = "".concat(nt.replacementClass, "-title-").concat(s || ot()) : (l["aria-hidden"] = "true", 
            l.focusable = "false")), on({
                icons: {
                    main: ln(d),
                    mask: r ? ln(r.icon) : {
                        found: !1,
                        width: null,
                        height: null,
                        icon: {}
                    }
                },
                prefix: u,
                iconName: m,
                transform: {
                    ...rt,
                    ...e
                },
                symbol: a,
                title: o,
                maskId: i,
                titleId: s,
                extra: {
                    attributes: l,
                    styles: f,
                    classes: c
                }
            })));
        }
    }
    x = {
        mixout() {
            return {
                icon: (a = Ln, function(t) {
                    var n = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {}, t = (t || {}).icon ? t : tn(t || {});
                    let e = n["mask"];
                    return e = e && ((e || {}).icon ? e : tn(e || {})), a(t, {
                        ...n,
                        mask: e
                    });
                })
            };
            var a;
        },
        hooks() {
            return {
                mutationObserverCallbacks(t) {
                    return t.treeCallback = jn, t.nodeCallback = Fn, t;
                }
            };
        },
        provides(t) {
            t.i2svg = function(t) {
                var {
                    node: n = w,
                    callback: t = () => {}
                } = t;
                return jn(n, t);
            }, t.generateSvgReplacementMutation = function(a, t) {
                const {
                    iconName: r,
                    title: i,
                    titleId: o,
                    prefix: s,
                    transform: c,
                    symbol: l,
                    mask: n,
                    maskId: f,
                    extra: u
                } = t;
                return new Promise((e, t) => {
                    Promise.all([ un(r, s), n.iconName ? un(n.iconName, n.prefix) : Promise.resolve({
                        found: !1,
                        width: 512,
                        height: 512,
                        icon: {}
                    }) ]).then(t => {
                        var [ n, t ] = t;
                        e([ a, on({
                            icons: {
                                main: n,
                                mask: t
                            },
                            prefix: s,
                            iconName: r,
                            transform: c,
                            symbol: l,
                            maskId: f,
                            title: i,
                            titleId: o,
                            extra: u,
                            watchable: !0
                        }) ]);
                    }).catch(t);
                });
            }, t.generateAbstractIcon = function(t) {
                let {
                    children: n,
                    attributes: e,
                    main: a,
                    transform: r,
                    styles: i
                } = t;
                t = ft(i);
                0 < t.length && (e.style = t);
                let o;
                return ut(r) && (o = $t("generateAbstractTransformGrouping", {
                    main: a,
                    transform: r,
                    containerWidth: a.width,
                    iconWidth: a.width
                })), n.push(o || a.icon), {
                    children: n,
                    attributes: e
                };
            };
        }
    }, N = {
        mixout() {
            return {
                layer(t) {
                    let e = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
                    const {
                        classes: a = []
                    } = e;
                    return rn({
                        type: "layer"
                    }, () => {
                        Zt("beforeDOMElementCreation", {
                            assembler: t,
                            params: e
                        });
                        let n = [];
                        return t(t => {
                            Array.isArray(t) ? t.map(t => {
                                n = n.concat(t.abstract);
                            }) : n = n.concat(t.abstract);
                        }), [ {
                            tag: "span",
                            attributes: {
                                class: [ "".concat(nt.cssPrefix, "-layers"), ...a ].join(" ")
                            },
                            children: n
                        } ];
                    });
                }
            };
        }
    }, o = {
        mixout() {
            return {
                counter(t) {
                    let n = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
                    const {
                        title: e = null,
                        classes: a = [],
                        attributes: r = {},
                        styles: i = {}
                    } = n;
                    return rn({
                        type: "counter",
                        content: t
                    }, () => (Zt("beforeDOMElementCreation", {
                        content: t,
                        params: n
                    }), function(t) {
                        const {
                            content: n,
                            title: e,
                            extra: a
                        } = t, r = {
                            ...a.attributes,
                            ...e ? {
                                title: e
                            } : {},
                            class: a.classes.join(" ")
                        };
                        0 < (t = ft(a.styles)).length && (r.style = t);
                        const i = [];
                        return i.push({
                            tag: "span",
                            attributes: r,
                            children: [ n ]
                        }), e && i.push({
                            tag: "span",
                            attributes: {
                                class: "sr-only"
                            },
                            children: [ e ]
                        }), i;
                    }({
                        content: t.toString(),
                        title: e,
                        extra: {
                            attributes: r,
                            styles: i,
                            classes: [ "".concat(nt.cssPrefix, "-layers-counter"), ...a ]
                        }
                    })));
                }
            };
        }
    }, y = {
        mixout() {
            return {
                text(t) {
                    let n = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
                    const {
                        transform: e = rt,
                        title: a = null,
                        classes: r = [],
                        attributes: i = {},
                        styles: o = {}
                    } = n;
                    return rn({
                        type: "text",
                        content: t
                    }, () => (Zt("beforeDOMElementCreation", {
                        content: t,
                        params: n
                    }), sn({
                        content: t,
                        transform: {
                            ...rt,
                            ...e
                        },
                        title: a,
                        extra: {
                            attributes: i,
                            styles: o,
                            classes: [ "".concat(nt.cssPrefix, "-layers-text"), ...r ]
                        }
                    })));
                }
            };
        },
        provides(t) {
            t.generateLayersText = function(t, n) {
                const {
                    title: e,
                    transform: a,
                    extra: r
                } = n;
                let i = null, o = null;
                var s;
                return u && (s = parseInt(getComputedStyle(t).fontSize, 10), n = t.getBoundingClientRect(), 
                i = n.width / s, o = n.height / s), nt.autoA11y && !e && (r.attributes["aria-hidden"] = "true"), 
                Promise.resolve([ t, sn({
                    content: t.innerHTML,
                    width: i,
                    height: o,
                    transform: a,
                    title: e,
                    extra: r,
                    watchable: !0
                }) ]);
            };
        }
    };
    const Rn = new RegExp('"', "ug"), In = [ 1105920, 1112319 ], Dn = {
        FontAwesome: {
            normal: "fas",
            400: "fas"
        },
        "Font Awesome 6 Free": {
            900: "fas",
            400: "far"
        },
        "Font Awesome 6 Pro": {
            900: "fas",
            400: "far",
            normal: "far",
            300: "fal",
            100: "fat"
        },
        "Font Awesome 6 Brands": {
            400: "fab",
            normal: "fab"
        },
        "Font Awesome 6 Duotone": {
            900: "fad"
        },
        "Font Awesome 6 Sharp": {
            900: "fass",
            400: "fasr",
            normal: "fasr",
            300: "fasl",
            100: "fast"
        },
        "Font Awesome 6 Sharp Duotone": {
            900: "fasds"
        },
        "Font Awesome 5 Free": {
            900: "fas",
            400: "far"
        },
        "Font Awesome 5 Pro": {
            900: "fas",
            400: "far",
            normal: "far",
            300: "fal"
        },
        "Font Awesome 5 Brands": {
            400: "fab",
            normal: "fab"
        },
        "Font Awesome 5 Duotone": {
            900: "fad"
        },
        "Font Awesome Kit": {
            400: "fak",
            normal: "fak"
        },
        "Font Awesome Kit Duotone": {
            400: "fakd",
            normal: "fakd"
        }
    }, Tn = Object.keys(Dn).reduce((t, n) => (t[n.toLowerCase()] = Dn[n], t), {}), Yn = Object.keys(Tn).reduce((t, n) => {
        var e = Tn[n];
        return t[n] = e[900] || [ ...Object.entries(e) ][0][1], t;
    }, {});
    function Hn(v, y) {
        const x = "".concat(E).concat(y.replace(":", "-"));
        return new Promise((i, n) => {
            if (null !== v.getAttribute(x)) return i();
            const t = st(v.children), e = t.filter(t => t.getAttribute(S) === y)[0], o = k.getComputedStyle(v, y), s = o.getPropertyValue("font-family"), c = s.match(G);
            var l, f, u = o.getPropertyValue("font-weight");
            const m = o.getPropertyValue("content");
            if (e && !c) return v.removeChild(e), i();
            if (c && "none" !== m && "" !== m) {
                const m = o.getPropertyValue("content");
                let a = (l = s, f = u, l = l.replace(/^['"]|['"]$/g, "").toLowerCase(), f = parseInt(f), 
                f = isNaN(f) ? "normal" : f, (Tn[l] || {})[f] || Yn[l]);
                var {
                    value: d,
                    isSecondary: p
                } = (h = m, d = h.replace(Rn, ""), u = 0, l = (f = d).length, h = (p = 55296 <= (h = f.charCodeAt(u)) && h <= 56319 && u + 1 < l && 56320 <= (p = f.charCodeAt(u + 1)) && p <= 57343 ? 1024 * (h - 55296) + p - 56320 + 65536 : h) >= In[0] && p <= In[1], 
                {
                    value: Ot((p = 2 === d.length && d[0] === d[1]) ? d[0] : d),
                    isSecondary: h || p
                }), h = c[0].startsWith("FontAwesome");
                let t = Ht(a, d), r = t;
                if (h && (h = d, d = Rt[h], h = Ht("fas", h), (h = d || (h ? {
                    prefix: "fas",
                    iconName: h
                } : null) || {
                    prefix: null,
                    iconName: null
                }).iconName && h.prefix && (t = h.iconName, a = h.prefix)), !t || p || e && e.getAttribute(M) === a && e.getAttribute(z) === r) i(); else {
                    v.setAttribute(x, r), e && v.removeChild(e);
                    const g = {
                        iconName: null,
                        title: null,
                        titleId: null,
                        prefix: null,
                        transform: rt,
                        symbol: !1,
                        mask: {
                            iconName: null,
                            prefix: null,
                            rest: []
                        },
                        maskId: null,
                        extra: {
                            classes: [],
                            styles: {},
                            attributes: {}
                        }
                    }, b = g["extra"];
                    b.attributes[S] = y, un(t, a).then(t => {
                        const n = on({
                            ...g,
                            icons: {
                                main: t,
                                mask: Bt()
                            },
                            prefix: a,
                            iconName: r,
                            extra: b,
                            watchable: !0
                        }), e = w.createElementNS("http://www.w3.org/2000/svg", "svg");
                        "::before" === y ? v.insertBefore(e, v.firstChild) : v.appendChild(e), e.outerHTML = n.map(t => kt(t)).join("\n"), 
                        v.removeAttribute(x), i();
                    }).catch(n);
                }
            } else i();
        });
    }
    function Wn(t) {
        return Promise.all([ Hn(t, "::before"), Hn(t, "::after") ]);
    }
    function _n(t) {
        return !(t.parentNode === document.head || ~L.indexOf(t.tagName.toUpperCase()) || t.getAttribute(S) || t.parentNode && "svg" === t.parentNode.tagName);
    }
    function Bn(r) {
        if (f) return new Promise((t, n) => {
            var e = st(r.querySelectorAll("*")).filter(_n).map(Wn);
            const a = hn.begin("searchPseudoElements");
            An(), Promise.all(e).then(() => {
                a(), Nn(), t();
            }).catch(() => {
                a(), Nn(), n();
            });
        });
    }
    let Un = !1;
    const Xn = t => {
        return t.toLowerCase().split(" ").reduce((t, n) => {
            const e = n.toLowerCase().split("-");
            n = e[0];
            let a = e.slice(1).join("-");
            if (n && "h" === a) return t.flipX = !0, t;
            if (n && "v" === a) return t.flipY = !0, t;
            if (a = parseFloat(a), isNaN(a)) return t;
            switch (n) {
              case "grow":
                t.size = t.size + a;
                break;

              case "shrink":
                t.size = t.size - a;
                break;

              case "left":
                t.x = t.x - a;
                break;

              case "right":
                t.x = t.x + a;
                break;

              case "up":
                t.y = t.y - a;
                break;

              case "down":
                t.y = t.y + a;
                break;

              case "rotate":
                t.rotate = t.rotate + a;
            }
            return t;
        }, {
            size: 16,
            x: 0,
            y: 0,
            flipX: !1,
            flipY: !1,
            rotate: 0
        });
    }, qn = {
        x: 0,
        y: 0,
        width: "100%",
        height: "100%"
    };
    function Vn(t) {
        return t.attributes && (t.attributes.fill || (!(1 < arguments.length && void 0 !== arguments[1]) || arguments[1])) && (t.attributes.fill = "black"), 
        t;
    }
    !function(t, n) {
        let a = n["mixoutsTo"];
        Vt = t, Gt = {}, Object.keys(Kt).forEach(t => {
            -1 === Jt.indexOf(t) && delete Kt[t];
        }), Vt.forEach(t => {
            const e = t.mixout ? t.mixout() : {};
            if (Object.keys(e).forEach(n => {
                "function" == typeof e[n] && (a[n] = e[n]), "object" == typeof e[n] && Object.keys(e[n]).forEach(t => {
                    a[n] || (a[n] = {}), a[n][t] = e[n][t];
                });
            }), t.hooks) {
                const n = t.hooks();
                Object.keys(n).forEach(t => {
                    Gt[t] || (Gt[t] = []), Gt[t].push(n[t]);
                });
            }
            t.provides && t.provides(Kt);
        }), a;
    }([ A, x, N, o, y, {
        hooks() {
            return {
                mutationObserverCallbacks(t) {
                    return t.pseudoElementsCallback = Bn, t;
                }
            };
        },
        provides(t) {
            t.pseudoElements2svg = function(t) {
                var {
                    node: t = w
                } = t;
                nt.searchPseudoElements && Bn(t);
            };
        }
    }, {
        mixout() {
            return {
                dom: {
                    unwatch() {
                        An(), Un = !0;
                    }
                }
            };
        },
        hooks() {
            return {
                bootstrap() {
                    Pn(Qt("mutationObserverCallbacks", {}));
                },
                noAuto() {
                    On && On.disconnect();
                },
                watch(t) {
                    t = t.observeMutationsRoot;
                    Un ? Nn() : Pn(Qt("mutationObserverCallbacks", {
                        observeMutationsRoot: t
                    }));
                }
            };
        }
    }, {
        mixout() {
            return {
                parse: {
                    transform: t => Xn(t)
                }
            };
        },
        hooks() {
            return {
                parseNodeAttributes(t, n) {
                    n = n.getAttribute("data-fa-transform");
                    return n && (t.transform = Xn(n)), t;
                }
            };
        },
        provides(t) {
            t.generateAbstractTransformGrouping = function(t) {
                var {
                    main: n,
                    transform: e,
                    containerWidth: a,
                    iconWidth: r
                } = t, i = {
                    transform: "translate(".concat(a / 2, " 256)")
                }, t = "translate(".concat(32 * e.x, ", ").concat(32 * e.y, ") "), a = "scale(".concat(e.size / 16 * (e.flipX ? -1 : 1), ", ").concat(e.size / 16 * (e.flipY ? -1 : 1), ") "), e = "rotate(".concat(e.rotate, " 0 0)");
                const o = i, s = {
                    transform: "".concat(t, " ").concat(a, " ").concat(e)
                }, c = {
                    transform: "translate(".concat(r / 2 * -1, " -256)")
                };
                return {
                    tag: "g",
                    attributes: {
                        ...o
                    },
                    children: [ {
                        tag: "g",
                        attributes: {
                            ...s
                        },
                        children: [ {
                            tag: n.icon.tag,
                            children: n.icon.children,
                            attributes: {
                                ...n.icon.attributes,
                                ...c
                            }
                        } ]
                    } ]
                };
            };
        }
    }, {
        hooks() {
            return {
                parseNodeAttributes(t, n) {
                    const e = n.getAttribute("data-fa-mask"), a = e ? qt(e.split(" ").map(t => t.trim())) : Bt();
                    return a.prefix || (a.prefix = zt), t.mask = a, t.maskId = n.getAttribute("data-fa-mask-id"), 
                    t;
                }
            };
        },
        provides(t) {
            t.generateAbstractMask = function(t) {
                let {
                    children: n,
                    attributes: e,
                    main: a,
                    mask: r,
                    maskId: i,
                    transform: o
                } = t;
                const {
                    width: s,
                    icon: c
                } = a;
                var {
                    width: l,
                    icon: f
                } = r, u = function(t) {
                    var {
                        transform: n,
                        containerWidth: e,
                        iconWidth: a
                    } = t, r = {
                        transform: "translate(".concat(e / 2, " 256)")
                    }, t = "translate(".concat(32 * n.x, ", ").concat(32 * n.y, ") "), e = "scale(".concat(n.size / 16 * (n.flipX ? -1 : 1), ", ").concat(n.size / 16 * (n.flipY ? -1 : 1), ") "), n = "rotate(".concat(n.rotate, " 0 0)");
                    return {
                        outer: r,
                        inner: {
                            transform: "".concat(t, " ").concat(e, " ").concat(n)
                        },
                        path: {
                            transform: "translate(".concat(a / 2 * -1, " -256)")
                        }
                    };
                }({
                    transform: o,
                    containerWidth: l,
                    iconWidth: s
                }), m = {
                    tag: "rect",
                    attributes: {
                        ...qn,
                        fill: "white"
                    }
                }, t = c.children ? {
                    children: c.children.map(Vn)
                } : {}, l = {
                    tag: "g",
                    attributes: {
                        ...u.inner
                    },
                    children: [ Vn({
                        tag: c.tag,
                        attributes: {
                            ...c.attributes,
                            ...u.path
                        },
                        ...t
                    }) ]
                }, t = {
                    tag: "g",
                    attributes: {
                        ...u.outer
                    },
                    children: [ l ]
                }, u = "mask-".concat(i || ot()), l = "clip-".concat(i || ot()), t = {
                    tag: "mask",
                    attributes: {
                        ...qn,
                        id: u,
                        maskUnits: "userSpaceOnUse",
                        maskContentUnits: "userSpaceOnUse"
                    },
                    children: [ m, t ]
                }, t = {
                    tag: "defs",
                    children: [ {
                        tag: "clipPath",
                        attributes: {
                            id: l
                        },
                        children: "g" === (f = f).tag ? f.children : [ f ]
                    }, t ]
                };
                return n.push(t, {
                    tag: "rect",
                    attributes: {
                        fill: "currentColor",
                        "clip-path": "url(#".concat(l, ")"),
                        mask: "url(#".concat(u, ")"),
                        ...qn
                    }
                }), {
                    children: n,
                    attributes: e
                };
            };
        }
    }, {
        provides(t) {
            let i = !1;
            k.matchMedia && (i = k.matchMedia("(prefers-reduced-motion: reduce)").matches), 
            t.missingIconAbstract = function() {
                const t = [];
                var n = {
                    fill: "currentColor"
                }, e = {
                    attributeType: "XML",
                    repeatCount: "indefinite",
                    dur: "2s"
                };
                t.push({
                    tag: "path",
                    attributes: {
                        ...n,
                        d: "M156.5,447.7l-12.6,29.5c-18.7-9.5-35.9-21.2-51.5-34.9l22.7-22.7C127.6,430.5,141.5,440,156.5,447.7z M40.6,272H8.5 c1.4,21.2,5.4,41.7,11.7,61.1L50,321.2C45.1,305.5,41.8,289,40.6,272z M40.6,240c1.4-18.8,5.2-37,11.1-54.1l-29.5-12.6 C14.7,194.3,10,216.7,8.5,240H40.6z M64.3,156.5c7.8-14.9,17.2-28.8,28.1-41.5L69.7,92.3c-13.7,15.6-25.5,32.8-34.9,51.5 L64.3,156.5z M397,419.6c-13.9,12-29.4,22.3-46.1,30.4l11.9,29.8c20.7-9.9,39.8-22.6,56.9-37.6L397,419.6z M115,92.4 c13.9-12,29.4-22.3,46.1-30.4l-11.9-29.8c-20.7,9.9-39.8,22.6-56.8,37.6L115,92.4z M447.7,355.5c-7.8,14.9-17.2,28.8-28.1,41.5 l22.7,22.7c13.7-15.6,25.5-32.9,34.9-51.5L447.7,355.5z M471.4,272c-1.4,18.8-5.2,37-11.1,54.1l29.5,12.6 c7.5-21.1,12.2-43.5,13.6-66.8H471.4z M321.2,462c-15.7,5-32.2,8.2-49.2,9.4v32.1c21.2-1.4,41.7-5.4,61.1-11.7L321.2,462z M240,471.4c-18.8-1.4-37-5.2-54.1-11.1l-12.6,29.5c21.1,7.5,43.5,12.2,66.8,13.6V471.4z M462,190.8c5,15.7,8.2,32.2,9.4,49.2h32.1 c-1.4-21.2-5.4-41.7-11.7-61.1L462,190.8z M92.4,397c-12-13.9-22.3-29.4-30.4-46.1l-29.8,11.9c9.9,20.7,22.6,39.8,37.6,56.9 L92.4,397z M272,40.6c18.8,1.4,36.9,5.2,54.1,11.1l12.6-29.5C317.7,14.7,295.3,10,272,8.5V40.6z M190.8,50 c15.7-5,32.2-8.2,49.2-9.4V8.5c-21.2,1.4-41.7,5.4-61.1,11.7L190.8,50z M442.3,92.3L419.6,115c12,13.9,22.3,29.4,30.5,46.1 l29.8-11.9C470,128.5,457.3,109.4,442.3,92.3z M397,92.4l22.7-22.7c-15.6-13.7-32.8-25.5-51.5-34.9l-12.6,29.5 C370.4,72.1,384.4,81.5,397,92.4z"
                    }
                });
                var a = {
                    ...e,
                    attributeName: "opacity"
                };
                const r = {
                    tag: "circle",
                    attributes: {
                        ...n,
                        cx: "256",
                        cy: "364",
                        r: "28"
                    },
                    children: []
                };
                return i || r.children.push({
                    tag: "animate",
                    attributes: {
                        ...e,
                        attributeName: "r",
                        values: "28;14;28;28;14;28;"
                    }
                }, {
                    tag: "animate",
                    attributes: {
                        ...a,
                        values: "1;0;1;1;0;1;"
                    }
                }), t.push(r), t.push({
                    tag: "path",
                    attributes: {
                        ...n,
                        opacity: "1",
                        d: "M263.7,312h-16c-6.6,0-12-5.4-12-12c0-71,77.4-63.9,77.4-107.8c0-20-17.8-40.2-57.4-40.2c-29.1,0-44.3,9.6-59.2,28.7 c-3.9,5-11.1,6-16.2,2.4l-13.1-9.2c-5.6-3.9-6.9-11.8-2.6-17.2c21.2-27.2,46.4-44.7,91.2-44.7c52.3,0,97.4,29.8,97.4,80.2 c0,67.6-77.4,63.5-77.4,107.8C275.7,306.6,270.3,312,263.7,312z"
                    },
                    children: i ? [] : [ {
                        tag: "animate",
                        attributes: {
                            ...a,
                            values: "1;0;0;0;0;1;"
                        }
                    } ]
                }), i || t.push({
                    tag: "path",
                    attributes: {
                        ...n,
                        opacity: "0",
                        d: "M232.5,134.5l7,168c0.3,6.4,5.6,11.5,12,11.5h9c6.4,0,11.7-5.1,12-11.5l7-168c0.3-6.8-5.2-12.5-12-12.5h-23 C237.7,122,232.2,127.7,232.5,134.5z"
                    },
                    children: [ {
                        tag: "animate",
                        attributes: {
                            ...a,
                            values: "0;0;1;1;0;0;"
                        }
                    } ]
                }), {
                    tag: "g",
                    attributes: {
                        class: "missing"
                    },
                    children: t
                };
            };
        }
    }, {
        hooks() {
            return {
                parseNodeAttributes(t, n) {
                    n = n.getAttribute("data-fa-symbol");
                    return t.symbol = null !== n && ("" === n || n), t;
                }
            };
        }
    } ], {
        mixoutsTo: en
    }), function(t) {
        try {
            for (var n = arguments.length, e = new Array(1 < n ? n - 1 : 0), a = 1; a < n; a++) e[a - 1] = arguments[a];
            t(...e);
        } catch (t) {
            if (!R) throw t;
        }
    }(function(t) {
        s && (k.FontAwesome || (k.FontAwesome = en), xt(() => {
            an(), Zt("bootstrap");
        })), gt.hooks = {
            ...gt.hooks,
            addPack: (t, n) => {
                gt.styles[t] = {
                    ...gt.styles[t] || {},
                    ...n
                }, Yt(), an();
            },
            addPacks: t => {
                t.forEach(t => {
                    var [ n, t ] = t;
                    gt.styles[n] = {
                        ...gt.styles[n] || {},
                        ...t
                    };
                }), Yt(), an();
            },
            addShims: t => {
                gt.shims.push(...t), Yt(), an();
            }
        };
    });
}();