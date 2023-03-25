/**
  * bootstrap-table - An extended table to integration with some of the most widely used CSS frameworks. (Supports Bootstrap, Semantic UI, Bulma, Material Design, Foundation)
  *
  * @version v1.21.1
  * @homepage https://bootstrap-table.com
  * @author wenzhixin <wenzhixin2010@gmail.com> (http://wenzhixin.net.cn/)
  * @license MIT
  */

!function(t,n){"object"==typeof exports&&"undefined"!=typeof module?n(require("jquery")):"function"==typeof define&&define.amd?define(["jquery"],n):n((t="undefined"!=typeof globalThis?globalThis:t||self).jQuery)}(this,(function(t){"use strict";function n(t){return t&&"object"==typeof t&&"default"in t?t:{default:t}}var r=n(t),e="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},o=function(t){return t&&t.Math==Math&&t},i=o("object"==typeof globalThis&&globalThis)||o("object"==typeof window&&window)||o("object"==typeof self&&self)||o("object"==typeof e&&e)||function(){return this}()||Function("return this")(),u={},c=function(t){try{return!!t()}catch(t){return!0}},a=!c((function(){return 7!=Object.defineProperty({},1,{get:function(){return 7}})[1]})),f=!c((function(){var t=function(){}.bind();return"function"!=typeof t||t.hasOwnProperty("prototype")})),l=f,s=Function.prototype.call,p=l?s.bind(s):function(){return s.apply(s,arguments)},y={},g={}.propertyIsEnumerable,d=Object.getOwnPropertyDescriptor,b=d&&!g.call({1:2},1);y.f=b?function(t){var n=d(this,t);return!!n&&n.enumerable}:g;var m,h,v=function(t,n){return{enumerable:!(1&t),configurable:!(2&t),writable:!(4&t),value:n}},w=f,S=Function.prototype,O=S.bind,j=S.call,P=w&&O.bind(j,j),T=w?function(t){return t&&P(t)}:function(t){return t&&function(){return j.apply(t,arguments)}},x=T,E=x({}.toString),A=x("".slice),C=function(t){return A(E(t),8,-1)},F=c,R=C,k=Object,M=T("".split),I=F((function(){return!k("z").propertyIsEnumerable(0)}))?function(t){return"String"==R(t)?M(t,""):k(t)}:k,D=TypeError,L=function(t){if(null==t)throw D("Can't call method on "+t);return t},N=I,z=L,G=function(t){return N(z(t))},_=function(t){return"function"==typeof t},H=_,q=function(t){return"object"==typeof t?null!==t:H(t)},B=i,K=_,U=function(t){return K(t)?t:void 0},V=function(t,n){return arguments.length<2?U(B[t]):B[t]&&B[t][n]},W=T({}.isPrototypeOf),J=i,Q=V("navigator","userAgent")||"",X=J.process,Y=J.Deno,$=X&&X.versions||Y&&Y.version,Z=$&&$.v8;Z&&(h=(m=Z.split("."))[0]>0&&m[0]<4?1:+(m[0]+m[1])),!h&&Q&&(!(m=Q.match(/Edge\/(\d+)/))||m[1]>=74)&&(m=Q.match(/Chrome\/(\d+)/))&&(h=+m[1]);var tt=h,nt=tt,rt=c,et=!!Object.getOwnPropertySymbols&&!rt((function(){var t=Symbol();return!String(t)||!(Object(t)instanceof Symbol)||!Symbol.sham&&nt&&nt<41})),ot=et&&!Symbol.sham&&"symbol"==typeof Symbol.iterator,it=V,ut=_,ct=W,at=Object,ft=ot?function(t){return"symbol"==typeof t}:function(t){var n=it("Symbol");return ut(n)&&ct(n.prototype,at(t))},lt=String,st=_,pt=function(t){try{return lt(t)}catch(t){return"Object"}},yt=TypeError,gt=function(t){if(st(t))return t;throw yt(pt(t)+" is not a function")},dt=p,bt=_,mt=q,ht=TypeError,vt={exports:{}},wt=i,St=Object.defineProperty,Ot=function(t,n){try{St(wt,t,{value:n,configurable:!0,writable:!0})}catch(r){wt[t]=n}return n},jt=Ot,Pt="__core-js_shared__",Tt=i[Pt]||jt(Pt,{}),xt=Tt;(vt.exports=function(t,n){return xt[t]||(xt[t]=void 0!==n?n:{})})("versions",[]).push({version:"3.22.8",mode:"global",copyright:"© 2014-2022 Denis Pushkarev (zloirock.ru)",license:"https://github.com/zloirock/core-js/blob/v3.22.8/LICENSE",source:"https://github.com/zloirock/core-js"});var Et=L,At=Object,Ct=function(t){return At(Et(t))},Ft=Ct,Rt=T({}.hasOwnProperty),kt=Object.hasOwn||function(t,n){return Rt(Ft(t),n)},Mt=T,It=0,Dt=Math.random(),Lt=Mt(1..toString),Nt=function(t){return"Symbol("+(void 0===t?"":t)+")_"+Lt(++It+Dt,36)},zt=i,Gt=vt.exports,_t=kt,Ht=Nt,qt=et,Bt=ot,Kt=Gt("wks"),Ut=zt.Symbol,Vt=Ut&&Ut.for,Wt=Bt?Ut:Ut&&Ut.withoutSetter||Ht,Jt=function(t){if(!_t(Kt,t)||!qt&&"string"!=typeof Kt[t]){var n="Symbol."+t;qt&&_t(Ut,t)?Kt[t]=Ut[t]:Kt[t]=Bt&&Vt?Vt(n):Wt(n)}return Kt[t]},Qt=p,Xt=q,Yt=ft,$t=function(t,n){var r=t[n];return null==r?void 0:gt(r)},Zt=function(t,n){var r,e;if("string"===n&&bt(r=t.toString)&&!mt(e=dt(r,t)))return e;if(bt(r=t.valueOf)&&!mt(e=dt(r,t)))return e;if("string"!==n&&bt(r=t.toString)&&!mt(e=dt(r,t)))return e;throw ht("Can't convert object to primitive value")},tn=TypeError,nn=Jt("toPrimitive"),rn=function(t,n){if(!Xt(t)||Yt(t))return t;var r,e=$t(t,nn);if(e){if(void 0===n&&(n="default"),r=Qt(e,t,n),!Xt(r)||Yt(r))return r;throw tn("Can't convert object to primitive value")}return void 0===n&&(n="number"),Zt(t,n)},en=ft,on=function(t){var n=rn(t,"string");return en(n)?n:n+""},un=q,cn=i.document,an=un(cn)&&un(cn.createElement),fn=function(t){return an?cn.createElement(t):{}},ln=!a&&!c((function(){return 7!=Object.defineProperty(fn("div"),"a",{get:function(){return 7}}).a})),sn=a,pn=p,yn=y,gn=v,dn=G,bn=on,mn=kt,hn=ln,vn=Object.getOwnPropertyDescriptor;u.f=sn?vn:function(t,n){if(t=dn(t),n=bn(n),hn)try{return vn(t,n)}catch(t){}if(mn(t,n))return gn(!pn(yn.f,t,n),t[n])};var wn={},Sn=a&&c((function(){return 42!=Object.defineProperty((function(){}),"prototype",{value:42,writable:!1}).prototype})),On=q,jn=String,Pn=TypeError,Tn=function(t){if(On(t))return t;throw Pn(jn(t)+" is not an object")},xn=a,En=ln,An=Sn,Cn=Tn,Fn=on,Rn=TypeError,kn=Object.defineProperty,Mn=Object.getOwnPropertyDescriptor,In="enumerable",Dn="configurable",Ln="writable";wn.f=xn?An?function(t,n,r){if(Cn(t),n=Fn(n),Cn(r),"function"==typeof t&&"prototype"===n&&"value"in r&&Ln in r&&!r.writable){var e=Mn(t,n);e&&e.writable&&(t[n]=r.value,r={configurable:Dn in r?r.configurable:e.configurable,enumerable:In in r?r.enumerable:e.enumerable,writable:!1})}return kn(t,n,r)}:kn:function(t,n,r){if(Cn(t),n=Fn(n),Cn(r),En)try{return kn(t,n,r)}catch(t){}if("get"in r||"set"in r)throw Rn("Accessors not supported");return"value"in r&&(t[n]=r.value),t};var Nn=wn,zn=v,Gn=a?function(t,n,r){return Nn.f(t,n,zn(1,r))}:function(t,n,r){return t[n]=r,t},_n={exports:{}},Hn=a,qn=kt,Bn=Function.prototype,Kn=Hn&&Object.getOwnPropertyDescriptor,Un=qn(Bn,"name"),Vn={EXISTS:Un,PROPER:Un&&"something"===function(){}.name,CONFIGURABLE:Un&&(!Hn||Hn&&Kn(Bn,"name").configurable)},Wn=_,Jn=Tt,Qn=T(Function.toString);Wn(Jn.inspectSource)||(Jn.inspectSource=function(t){return Qn(t)});var Xn,Yn,$n,Zn=Jn.inspectSource,tr=_,nr=Zn,rr=i.WeakMap,er=tr(rr)&&/native code/.test(nr(rr)),or=vt.exports,ir=Nt,ur=or("keys"),cr={},ar=er,fr=i,lr=T,sr=q,pr=Gn,yr=kt,gr=Tt,dr=function(t){return ur[t]||(ur[t]=ir(t))},br=cr,mr="Object already initialized",hr=fr.TypeError,vr=fr.WeakMap;if(ar||gr.state){var wr=gr.state||(gr.state=new vr),Sr=lr(wr.get),Or=lr(wr.has),jr=lr(wr.set);Xn=function(t,n){if(Or(wr,t))throw new hr(mr);return n.facade=t,jr(wr,t,n),n},Yn=function(t){return Sr(wr,t)||{}},$n=function(t){return Or(wr,t)}}else{var Pr=dr("state");br[Pr]=!0,Xn=function(t,n){if(yr(t,Pr))throw new hr(mr);return n.facade=t,pr(t,Pr,n),n},Yn=function(t){return yr(t,Pr)?t[Pr]:{}},$n=function(t){return yr(t,Pr)}}var Tr={set:Xn,get:Yn,has:$n,enforce:function(t){return $n(t)?Yn(t):Xn(t,{})},getterFor:function(t){return function(n){var r;if(!sr(n)||(r=Yn(n)).type!==t)throw hr("Incompatible receiver, "+t+" required");return r}}},xr=c,Er=_,Ar=kt,Cr=a,Fr=Vn.CONFIGURABLE,Rr=Zn,kr=Tr.enforce,Mr=Tr.get,Ir=Object.defineProperty,Dr=Cr&&!xr((function(){return 8!==Ir((function(){}),"length",{value:8}).length})),Lr=String(String).split("String"),Nr=_n.exports=function(t,n,r){"Symbol("===String(n).slice(0,7)&&(n="["+String(n).replace(/^Symbol\(([^)]*)\)/,"$1")+"]"),r&&r.getter&&(n="get "+n),r&&r.setter&&(n="set "+n),(!Ar(t,"name")||Fr&&t.name!==n)&&Ir(t,"name",{value:n,configurable:!0}),Dr&&r&&Ar(r,"arity")&&t.length!==r.arity&&Ir(t,"length",{value:r.arity});try{r&&Ar(r,"constructor")&&r.constructor?Cr&&Ir(t,"prototype",{writable:!1}):t.prototype&&(t.prototype=void 0)}catch(t){}var e=kr(t);return Ar(e,"source")||(e.source=Lr.join("string"==typeof n?n:"")),t};Function.prototype.toString=Nr((function(){return Er(this)&&Mr(this).source||Rr(this)}),"toString");var zr=_,Gr=Gn,_r=_n.exports,Hr=Ot,qr={},Br=Math.ceil,Kr=Math.floor,Ur=Math.trunc||function(t){var n=+t;return(n>0?Kr:Br)(n)},Vr=function(t){var n=+t;return n!=n||0===n?0:Ur(n)},Wr=Vr,Jr=Math.max,Qr=Math.min,Xr=Vr,Yr=Math.min,$r=function(t){return t>0?Yr(Xr(t),9007199254740991):0},Zr=function(t){return $r(t.length)},te=G,ne=function(t,n){var r=Wr(t);return r<0?Jr(r+n,0):Qr(r,n)},re=Zr,ee=function(t){return function(n,r,e){var o,i=te(n),u=re(i),c=ne(e,u);if(t&&r!=r){for(;u>c;)if((o=i[c++])!=o)return!0}else for(;u>c;c++)if((t||c in i)&&i[c]===r)return t||c||0;return!t&&-1}},oe={includes:ee(!0),indexOf:ee(!1)},ie=kt,ue=G,ce=oe.indexOf,ae=cr,fe=T([].push),le=function(t,n){var r,e=ue(t),o=0,i=[];for(r in e)!ie(ae,r)&&ie(e,r)&&fe(i,r);for(;n.length>o;)ie(e,r=n[o++])&&(~ce(i,r)||fe(i,r));return i},se=["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"].concat("length","prototype");qr.f=Object.getOwnPropertyNames||function(t){return le(t,se)};var pe={};pe.f=Object.getOwnPropertySymbols;var ye=V,ge=qr,de=pe,be=Tn,me=T([].concat),he=ye("Reflect","ownKeys")||function(t){var n=ge.f(be(t)),r=de.f;return r?me(n,r(t)):n},ve=kt,we=he,Se=u,Oe=wn,je=c,Pe=_,Te=/#|\.prototype\./,xe=function(t,n){var r=Ae[Ee(t)];return r==Fe||r!=Ce&&(Pe(n)?je(n):!!n)},Ee=xe.normalize=function(t){return String(t).replace(Te,".").toLowerCase()},Ae=xe.data={},Ce=xe.NATIVE="N",Fe=xe.POLYFILL="P",Re=xe,ke=i,Me=u.f,Ie=Gn,De=function(t,n,r,e){e||(e={});var o=e.enumerable,i=void 0!==e.name?e.name:n;return zr(r)&&_r(r,i,e),e.global?o?t[n]=r:Hr(n,r):(e.unsafe?t[n]&&(o=!0):delete t[n],o?t[n]=r:Gr(t,n,r)),t},Le=Ot,Ne=function(t,n,r){for(var e=we(n),o=Oe.f,i=Se.f,u=0;u<e.length;u++){var c=e[u];ve(t,c)||r&&ve(r,c)||o(t,c,i(n,c))}},ze=Re,Ge=C,_e=Array.isArray||function(t){return"Array"==Ge(t)},He=TypeError,qe=on,Be=wn,Ke=v,Ue={};Ue[Jt("toStringTag")]="z";var Ve="[object z]"===String(Ue),We=_,Je=C,Qe=Jt("toStringTag"),Xe=Object,Ye="Arguments"==Je(function(){return arguments}()),$e=T,Ze=c,to=_,no=Ve?Je:function(t){var n,r,e;return void 0===t?"Undefined":null===t?"Null":"string"==typeof(r=function(t,n){try{return t[n]}catch(t){}}(n=Xe(t),Qe))?r:Ye?Je(n):"Object"==(e=Je(n))&&We(n.callee)?"Arguments":e},ro=Zn,eo=function(){},oo=[],io=V("Reflect","construct"),uo=/^\s*(?:class|function)\b/,co=$e(uo.exec),ao=!uo.exec(eo),fo=function(t){if(!to(t))return!1;try{return io(eo,oo,t),!0}catch(t){return!1}},lo=function(t){if(!to(t))return!1;switch(no(t)){case"AsyncFunction":case"GeneratorFunction":case"AsyncGeneratorFunction":return!1}try{return ao||!!co(uo,ro(t))}catch(t){return!0}};lo.sham=!0;var so=!io||Ze((function(){var t;return fo(fo.call)||!fo(Object)||!fo((function(){t=!0}))||t}))?lo:fo,po=_e,yo=so,go=q,bo=Jt("species"),mo=Array,ho=function(t){var n;return po(t)&&(n=t.constructor,(yo(n)&&(n===mo||po(n.prototype))||go(n)&&null===(n=n[bo]))&&(n=void 0)),void 0===n?mo:n},vo=c,wo=tt,So=Jt("species"),Oo=function(t,n){var r,e,o,i,u,c=t.target,a=t.global,f=t.stat;if(r=a?ke:f?ke[c]||Le(c,{}):(ke[c]||{}).prototype)for(e in n){if(i=n[e],o=t.dontCallGetSet?(u=Me(r,e))&&u.value:r[e],!ze(a?e:c+(f?".":"#")+e,t.forced)&&void 0!==o){if(typeof i==typeof o)continue;Ne(i,o)}(t.sham||o&&o.sham)&&Ie(i,"sham",!0),De(r,e,i,t)}},jo=c,Po=_e,To=q,xo=Ct,Eo=Zr,Ao=function(t){if(t>9007199254740991)throw He("Maximum allowed index exceeded");return t},Co=function(t,n,r){var e=qe(n);e in t?Be.f(t,e,Ke(0,r)):t[e]=r},Fo=function(t,n){return new(ho(t))(0===n?0:n)},Ro=function(t){return wo>=51||!vo((function(){var n=[];return(n.constructor={})[So]=function(){return{foo:1}},1!==n[t](Boolean).foo}))},ko=tt,Mo=Jt("isConcatSpreadable"),Io=ko>=51||!jo((function(){var t=[];return t[Mo]=!1,t.concat()[0]!==t})),Do=Ro("concat"),Lo=function(t){if(!To(t))return!1;var n=t[Mo];return void 0!==n?!!n:Po(t)};Oo({target:"Array",proto:!0,arity:1,forced:!Io||!Do},{concat:function(t){var n,r,e,o,i,u=xo(this),c=Fo(u,0),a=0;for(n=-1,e=arguments.length;n<e;n++)if(Lo(i=-1===n?u:arguments[n]))for(o=Eo(i),Ao(a+o),r=0;r<o;r++,a++)r in i&&Co(c,a,i[r]);else Ao(a+1),Co(c,a++,i);return c.length=a,c}}),r.default.fn.bootstrapTable.locales["da-DK"]=r.default.fn.bootstrapTable.locales.da={formatCopyRows:function(){return"Copy Rows"},formatPrint:function(){return"Print"},formatLoadingMessage:function(){return"Indlæser, vent venligst"},formatRecordsPerPage:function(t){return"".concat(t," poster pr side")},formatShowingRows:function(t,n,r,e){return void 0!==e&&e>0&&e>r?"Viser ".concat(t," til ").concat(n," af ").concat(r," række").concat(r>1?"r":""," (filtered from ").concat(e," total rows)"):"Viser ".concat(t," til ").concat(n," af ").concat(r," række").concat(r>1?"r":"")},formatSRPaginationPreText:function(){return"previous page"},formatSRPaginationPageText:function(t){return"to page ".concat(t)},formatSRPaginationNextText:function(){return"next page"},formatDetailPagination:function(t){return"Viser ".concat(t," række").concat(t>1?"r":"")},formatClearSearch:function(){return"Ryd filtre"},formatSearch:function(){return"Søg"},formatNoMatches:function(){return"Ingen poster fundet"},formatPaginationSwitch:function(){return"Skjul/vis nummerering"},formatPaginationSwitchDown:function(){return"Show pagination"},formatPaginationSwitchUp:function(){return"Hide pagination"},formatRefresh:function(){return"Opdater"},formatToggleOn:function(){return"Show card view"},formatToggleOff:function(){return"Hide card view"},formatColumns:function(){return"Kolonner"},formatColumnsToggleAll:function(){return"Toggle all"},formatFullscreen:function(){return"Fullscreen"},formatAllRows:function(){return"Alle"},formatAutoRefresh:function(){return"Auto Refresh"},formatExport:function(){return"Eksporter"},formatJumpTo:function(){return"GO"},formatAdvancedSearch:function(){return"Advanced search"},formatAdvancedCloseButton:function(){return"Close"},formatFilterControlSwitch:function(){return"Hide/Show controls"},formatFilterControlSwitchHide:function(){return"Hide controls"},formatFilterControlSwitchShow:function(){return"Show controls"}},r.default.extend(r.default.fn.bootstrapTable.defaults,r.default.fn.bootstrapTable.locales["da-DK"])}));
