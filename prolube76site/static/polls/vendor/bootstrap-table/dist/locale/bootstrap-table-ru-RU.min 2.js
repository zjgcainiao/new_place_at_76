/**
  * bootstrap-table - An extended table to integration with some of the most widely used CSS frameworks. (Supports Bootstrap, Semantic UI, Bulma, Material Design, Foundation)
  *
  * @version v1.21.1
  * @homepage https://bootstrap-table.com
  * @author wenzhixin <wenzhixin2010@gmail.com> (http://wenzhixin.net.cn/)
  * @license MIT
  */

!function(t,n){"object"==typeof exports&&"undefined"!=typeof module?n(require("jquery")):"function"==typeof define&&define.amd?define(["jquery"],n):n((t="undefined"!=typeof globalThis?globalThis:t||self).jQuery)}(this,(function(t){"use strict";function n(t){return t&&"object"==typeof t&&"default"in t?t:{default:t}}var r=n(t),e="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},o=function(t){return t&&t.Math==Math&&t},i=o("object"==typeof globalThis&&globalThis)||o("object"==typeof window&&window)||o("object"==typeof self&&self)||o("object"==typeof e&&e)||function(){return this}()||Function("return this")(),u={},c=function(t){try{return!!t()}catch(t){return!0}},a=!c((function(){return 7!=Object.defineProperty({},1,{get:function(){return 7}})[1]})),f=!c((function(){var t=function(){}.bind();return"function"!=typeof t||t.hasOwnProperty("prototype")})),l=f,s=Function.prototype.call,p=l?s.bind(s):function(){return s.apply(s,arguments)},y={},b={}.propertyIsEnumerable,g=Object.getOwnPropertyDescriptor,m=g&&!b.call({1:2},1);y.f=m?function(t){var n=g(this,t);return!!n&&n.enumerable}:b;var h,d,v=function(t,n){return{enumerable:!(1&t),configurable:!(2&t),writable:!(4&t),value:n}},w=f,S=Function.prototype,O=S.bind,j=S.call,P=w&&O.bind(j,j),T=w?function(t){return t&&P(t)}:function(t){return t&&function(){return j.apply(t,arguments)}},x=T,E=x({}.toString),A=x("".slice),C=function(t){return A(E(t),8,-1)},F=c,R=C,M=Object,I=T("".split),L=F((function(){return!M("z").propertyIsEnumerable(0)}))?function(t){return"String"==R(t)?I(t,""):M(t)}:M,N=TypeError,k=function(t){if(null==t)throw N("Can't call method on "+t);return t},z=L,D=k,U=function(t){return z(D(t))},_=function(t){return"function"==typeof t},G=_,q=function(t){return"object"==typeof t?null!==t:G(t)},B=i,W=_,H=function(t){return W(t)?t:void 0},J=function(t,n){return arguments.length<2?H(B[t]):B[t]&&B[t][n]},K=T({}.isPrototypeOf),Q=i,V=J("navigator","userAgent")||"",X=Q.process,Y=Q.Deno,$=X&&X.versions||Y&&Y.version,Z=$&&$.v8;Z&&(d=(h=Z.split("."))[0]>0&&h[0]<4?1:+(h[0]+h[1])),!d&&V&&(!(h=V.match(/Edge\/(\d+)/))||h[1]>=74)&&(h=V.match(/Chrome\/(\d+)/))&&(d=+h[1]);var tt=d,nt=tt,rt=c,et=!!Object.getOwnPropertySymbols&&!rt((function(){var t=Symbol();return!String(t)||!(Object(t)instanceof Symbol)||!Symbol.sham&&nt&&nt<41})),ot=et&&!Symbol.sham&&"symbol"==typeof Symbol.iterator,it=J,ut=_,ct=K,at=Object,ft=ot?function(t){return"symbol"==typeof t}:function(t){var n=it("Symbol");return ut(n)&&ct(n.prototype,at(t))},lt=String,st=_,pt=function(t){try{return lt(t)}catch(t){return"Object"}},yt=TypeError,bt=function(t){if(st(t))return t;throw yt(pt(t)+" is not a function")},gt=p,mt=_,ht=q,dt=TypeError,vt={exports:{}},wt=i,St=Object.defineProperty,Ot=function(t,n){try{St(wt,t,{value:n,configurable:!0,writable:!0})}catch(r){wt[t]=n}return n},jt=Ot,Pt="__core-js_shared__",Tt=i[Pt]||jt(Pt,{}),xt=Tt;(vt.exports=function(t,n){return xt[t]||(xt[t]=void 0!==n?n:{})})("versions",[]).push({version:"3.22.8",mode:"global",copyright:"© 2014-2022 Denis Pushkarev (zloirock.ru)",license:"https://github.com/zloirock/core-js/blob/v3.22.8/LICENSE",source:"https://github.com/zloirock/core-js"});var Et=k,At=Object,Ct=function(t){return At(Et(t))},Ft=Ct,Rt=T({}.hasOwnProperty),Mt=Object.hasOwn||function(t,n){return Rt(Ft(t),n)},It=T,Lt=0,Nt=Math.random(),kt=It(1..toString),zt=function(t){return"Symbol("+(void 0===t?"":t)+")_"+kt(++Lt+Nt,36)},Dt=i,Ut=vt.exports,_t=Mt,Gt=zt,qt=et,Bt=ot,Wt=Ut("wks"),Ht=Dt.Symbol,Jt=Ht&&Ht.for,Kt=Bt?Ht:Ht&&Ht.withoutSetter||Gt,Qt=function(t){if(!_t(Wt,t)||!qt&&"string"!=typeof Wt[t]){var n="Symbol."+t;qt&&_t(Ht,t)?Wt[t]=Ht[t]:Wt[t]=Bt&&Jt?Jt(n):Kt(n)}return Wt[t]},Vt=p,Xt=q,Yt=ft,$t=function(t,n){var r=t[n];return null==r?void 0:bt(r)},Zt=function(t,n){var r,e;if("string"===n&&mt(r=t.toString)&&!ht(e=gt(r,t)))return e;if(mt(r=t.valueOf)&&!ht(e=gt(r,t)))return e;if("string"!==n&&mt(r=t.toString)&&!ht(e=gt(r,t)))return e;throw dt("Can't convert object to primitive value")},tn=TypeError,nn=Qt("toPrimitive"),rn=function(t,n){if(!Xt(t)||Yt(t))return t;var r,e=$t(t,nn);if(e){if(void 0===n&&(n="default"),r=Vt(e,t,n),!Xt(r)||Yt(r))return r;throw tn("Can't convert object to primitive value")}return void 0===n&&(n="number"),Zt(t,n)},en=ft,on=function(t){var n=rn(t,"string");return en(n)?n:n+""},un=q,cn=i.document,an=un(cn)&&un(cn.createElement),fn=function(t){return an?cn.createElement(t):{}},ln=!a&&!c((function(){return 7!=Object.defineProperty(fn("div"),"a",{get:function(){return 7}}).a})),sn=a,pn=p,yn=y,bn=v,gn=U,mn=on,hn=Mt,dn=ln,vn=Object.getOwnPropertyDescriptor;u.f=sn?vn:function(t,n){if(t=gn(t),n=mn(n),dn)try{return vn(t,n)}catch(t){}if(hn(t,n))return bn(!pn(yn.f,t,n),t[n])};var wn={},Sn=a&&c((function(){return 42!=Object.defineProperty((function(){}),"prototype",{value:42,writable:!1}).prototype})),On=q,jn=String,Pn=TypeError,Tn=function(t){if(On(t))return t;throw Pn(jn(t)+" is not an object")},xn=a,En=ln,An=Sn,Cn=Tn,Fn=on,Rn=TypeError,Mn=Object.defineProperty,In=Object.getOwnPropertyDescriptor,Ln="enumerable",Nn="configurable",kn="writable";wn.f=xn?An?function(t,n,r){if(Cn(t),n=Fn(n),Cn(r),"function"==typeof t&&"prototype"===n&&"value"in r&&kn in r&&!r.writable){var e=In(t,n);e&&e.writable&&(t[n]=r.value,r={configurable:Nn in r?r.configurable:e.configurable,enumerable:Ln in r?r.enumerable:e.enumerable,writable:!1})}return Mn(t,n,r)}:Mn:function(t,n,r){if(Cn(t),n=Fn(n),Cn(r),En)try{return Mn(t,n,r)}catch(t){}if("get"in r||"set"in r)throw Rn("Accessors not supported");return"value"in r&&(t[n]=r.value),t};var zn=wn,Dn=v,Un=a?function(t,n,r){return zn.f(t,n,Dn(1,r))}:function(t,n,r){return t[n]=r,t},_n={exports:{}},Gn=a,qn=Mt,Bn=Function.prototype,Wn=Gn&&Object.getOwnPropertyDescriptor,Hn=qn(Bn,"name"),Jn={EXISTS:Hn,PROPER:Hn&&"something"===function(){}.name,CONFIGURABLE:Hn&&(!Gn||Gn&&Wn(Bn,"name").configurable)},Kn=_,Qn=Tt,Vn=T(Function.toString);Kn(Qn.inspectSource)||(Qn.inspectSource=function(t){return Vn(t)});var Xn,Yn,$n,Zn=Qn.inspectSource,tr=_,nr=Zn,rr=i.WeakMap,er=tr(rr)&&/native code/.test(nr(rr)),or=vt.exports,ir=zt,ur=or("keys"),cr={},ar=er,fr=i,lr=T,sr=q,pr=Un,yr=Mt,br=Tt,gr=function(t){return ur[t]||(ur[t]=ir(t))},mr=cr,hr="Object already initialized",dr=fr.TypeError,vr=fr.WeakMap;if(ar||br.state){var wr=br.state||(br.state=new vr),Sr=lr(wr.get),Or=lr(wr.has),jr=lr(wr.set);Xn=function(t,n){if(Or(wr,t))throw new dr(hr);return n.facade=t,jr(wr,t,n),n},Yn=function(t){return Sr(wr,t)||{}},$n=function(t){return Or(wr,t)}}else{var Pr=gr("state");mr[Pr]=!0,Xn=function(t,n){if(yr(t,Pr))throw new dr(hr);return n.facade=t,pr(t,Pr,n),n},Yn=function(t){return yr(t,Pr)?t[Pr]:{}},$n=function(t){return yr(t,Pr)}}var Tr={set:Xn,get:Yn,has:$n,enforce:function(t){return $n(t)?Yn(t):Xn(t,{})},getterFor:function(t){return function(n){var r;if(!sr(n)||(r=Yn(n)).type!==t)throw dr("Incompatible receiver, "+t+" required");return r}}},xr=c,Er=_,Ar=Mt,Cr=a,Fr=Jn.CONFIGURABLE,Rr=Zn,Mr=Tr.enforce,Ir=Tr.get,Lr=Object.defineProperty,Nr=Cr&&!xr((function(){return 8!==Lr((function(){}),"length",{value:8}).length})),kr=String(String).split("String"),zr=_n.exports=function(t,n,r){"Symbol("===String(n).slice(0,7)&&(n="["+String(n).replace(/^Symbol\(([^)]*)\)/,"$1")+"]"),r&&r.getter&&(n="get "+n),r&&r.setter&&(n="set "+n),(!Ar(t,"name")||Fr&&t.name!==n)&&Lr(t,"name",{value:n,configurable:!0}),Nr&&r&&Ar(r,"arity")&&t.length!==r.arity&&Lr(t,"length",{value:r.arity});try{r&&Ar(r,"constructor")&&r.constructor?Cr&&Lr(t,"prototype",{writable:!1}):t.prototype&&(t.prototype=void 0)}catch(t){}var e=Mr(t);return Ar(e,"source")||(e.source=kr.join("string"==typeof n?n:"")),t};Function.prototype.toString=zr((function(){return Er(this)&&Ir(this).source||Rr(this)}),"toString");var Dr=_,Ur=Un,_r=_n.exports,Gr=Ot,qr={},Br=Math.ceil,Wr=Math.floor,Hr=Math.trunc||function(t){var n=+t;return(n>0?Wr:Br)(n)},Jr=function(t){var n=+t;return n!=n||0===n?0:Hr(n)},Kr=Jr,Qr=Math.max,Vr=Math.min,Xr=Jr,Yr=Math.min,$r=function(t){return t>0?Yr(Xr(t),9007199254740991):0},Zr=function(t){return $r(t.length)},te=U,ne=function(t,n){var r=Kr(t);return r<0?Qr(r+n,0):Vr(r,n)},re=Zr,ee=function(t){return function(n,r,e){var o,i=te(n),u=re(i),c=ne(e,u);if(t&&r!=r){for(;u>c;)if((o=i[c++])!=o)return!0}else for(;u>c;c++)if((t||c in i)&&i[c]===r)return t||c||0;return!t&&-1}},oe={includes:ee(!0),indexOf:ee(!1)},ie=Mt,ue=U,ce=oe.indexOf,ae=cr,fe=T([].push),le=function(t,n){var r,e=ue(t),o=0,i=[];for(r in e)!ie(ae,r)&&ie(e,r)&&fe(i,r);for(;n.length>o;)ie(e,r=n[o++])&&(~ce(i,r)||fe(i,r));return i},se=["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"].concat("length","prototype");qr.f=Object.getOwnPropertyNames||function(t){return le(t,se)};var pe={};pe.f=Object.getOwnPropertySymbols;var ye=J,be=qr,ge=pe,me=Tn,he=T([].concat),de=ye("Reflect","ownKeys")||function(t){var n=be.f(me(t)),r=ge.f;return r?he(n,r(t)):n},ve=Mt,we=de,Se=u,Oe=wn,je=c,Pe=_,Te=/#|\.prototype\./,xe=function(t,n){var r=Ae[Ee(t)];return r==Fe||r!=Ce&&(Pe(n)?je(n):!!n)},Ee=xe.normalize=function(t){return String(t).replace(Te,".").toLowerCase()},Ae=xe.data={},Ce=xe.NATIVE="N",Fe=xe.POLYFILL="P",Re=xe,Me=i,Ie=u.f,Le=Un,Ne=function(t,n,r,e){e||(e={});var o=e.enumerable,i=void 0!==e.name?e.name:n;return Dr(r)&&_r(r,i,e),e.global?o?t[n]=r:Gr(n,r):(e.unsafe?t[n]&&(o=!0):delete t[n],o?t[n]=r:Ur(t,n,r)),t},ke=Ot,ze=function(t,n,r){for(var e=we(n),o=Oe.f,i=Se.f,u=0;u<e.length;u++){var c=e[u];ve(t,c)||r&&ve(r,c)||o(t,c,i(n,c))}},De=Re,Ue=C,_e=Array.isArray||function(t){return"Array"==Ue(t)},Ge=TypeError,qe=on,Be=wn,We=v,He={};He[Qt("toStringTag")]="z";var Je="[object z]"===String(He),Ke=_,Qe=C,Ve=Qt("toStringTag"),Xe=Object,Ye="Arguments"==Qe(function(){return arguments}()),$e=T,Ze=c,to=_,no=Je?Qe:function(t){var n,r,e;return void 0===t?"Undefined":null===t?"Null":"string"==typeof(r=function(t,n){try{return t[n]}catch(t){}}(n=Xe(t),Ve))?r:Ye?Qe(n):"Object"==(e=Qe(n))&&Ke(n.callee)?"Arguments":e},ro=Zn,eo=function(){},oo=[],io=J("Reflect","construct"),uo=/^\s*(?:class|function)\b/,co=$e(uo.exec),ao=!uo.exec(eo),fo=function(t){if(!to(t))return!1;try{return io(eo,oo,t),!0}catch(t){return!1}},lo=function(t){if(!to(t))return!1;switch(no(t)){case"AsyncFunction":case"GeneratorFunction":case"AsyncGeneratorFunction":return!1}try{return ao||!!co(uo,ro(t))}catch(t){return!0}};lo.sham=!0;var so=!io||Ze((function(){var t;return fo(fo.call)||!fo(Object)||!fo((function(){t=!0}))||t}))?lo:fo,po=_e,yo=so,bo=q,go=Qt("species"),mo=Array,ho=function(t){var n;return po(t)&&(n=t.constructor,(yo(n)&&(n===mo||po(n.prototype))||bo(n)&&null===(n=n[go]))&&(n=void 0)),void 0===n?mo:n},vo=c,wo=tt,So=Qt("species"),Oo=function(t,n){var r,e,o,i,u,c=t.target,a=t.global,f=t.stat;if(r=a?Me:f?Me[c]||ke(c,{}):(Me[c]||{}).prototype)for(e in n){if(i=n[e],o=t.dontCallGetSet?(u=Ie(r,e))&&u.value:r[e],!De(a?e:c+(f?".":"#")+e,t.forced)&&void 0!==o){if(typeof i==typeof o)continue;ze(i,o)}(t.sham||o&&o.sham)&&Le(i,"sham",!0),Ne(r,e,i,t)}},jo=c,Po=_e,To=q,xo=Ct,Eo=Zr,Ao=function(t){if(t>9007199254740991)throw Ge("Maximum allowed index exceeded");return t},Co=function(t,n,r){var e=qe(n);e in t?Be.f(t,e,We(0,r)):t[e]=r},Fo=function(t,n){return new(ho(t))(0===n?0:n)},Ro=function(t){return wo>=51||!vo((function(){var n=[];return(n.constructor={})[So]=function(){return{foo:1}},1!==n[t](Boolean).foo}))},Mo=tt,Io=Qt("isConcatSpreadable"),Lo=Mo>=51||!jo((function(){var t=[];return t[Io]=!1,t.concat()[0]!==t})),No=Ro("concat"),ko=function(t){if(!To(t))return!1;var n=t[Io];return void 0!==n?!!n:Po(t)};Oo({target:"Array",proto:!0,arity:1,forced:!Lo||!No},{concat:function(t){var n,r,e,o,i,u=xo(this),c=Fo(u,0),a=0;for(n=-1,e=arguments.length;n<e;n++)if(ko(i=-1===n?u:arguments[n]))for(o=Eo(i),Ao(a+o),r=0;r<o;r++,a++)r in i&&Co(c,a,i[r]);else Ao(a+1),Co(c,a++,i);return c.length=a,c}}),r.default.fn.bootstrapTable.locales["ru-RU"]=r.default.fn.bootstrapTable.locales.ru={formatCopyRows:function(){return"Скопировать строки"},formatPrint:function(){return"Печать"},formatLoadingMessage:function(){return"Пожалуйста, подождите, идёт загрузка"},formatRecordsPerPage:function(t){return"".concat(t," записей на страницу")},formatShowingRows:function(t,n,r,e){return void 0!==e&&e>0&&e>r?"Записи с ".concat(t," по ").concat(n," из ").concat(r," (отфильтровано, всего на сервере ").concat(e," записей)"):"Записи с ".concat(t," по ").concat(n," из ").concat(r)},formatSRPaginationPreText:function(){return"предыдущая страница"},formatSRPaginationPageText:function(t){return"перейти к странице ".concat(t)},formatSRPaginationNextText:function(){return"следующая страница"},formatDetailPagination:function(t){return"Загружено ".concat(t," строк")},formatClearSearch:function(){return"Очистить фильтры"},formatSearch:function(){return"Поиск"},formatNoMatches:function(){return"Ничего не найдено"},formatPaginationSwitch:function(){return"Скрыть/Показать постраничную навигацию"},formatPaginationSwitchDown:function(){return"Показать постраничную навигацию"},formatPaginationSwitchUp:function(){return"Скрыть постраничную навигацию"},formatRefresh:function(){return"Обновить"},formatToggleOn:function(){return"Показать записи в виде карточек"},formatToggleOff:function(){return"Табличный режим просмотра"},formatColumns:function(){return"Колонки"},formatColumnsToggleAll:function(){return"Выбрать все"},formatFullscreen:function(){return"Полноэкранный режим"},formatAllRows:function(){return"Все"},formatAutoRefresh:function(){return"Автоматическое обновление"},formatExport:function(){return"Экспортировать данные"},formatJumpTo:function(){return"Стр."},formatAdvancedSearch:function(){return"Расширенный поиск"},formatAdvancedCloseButton:function(){return"Закрыть"},formatFilterControlSwitch:function(){return"Скрыть/Показать панель инструментов"},formatFilterControlSwitchHide:function(){return"Скрыть панель инструментов"},formatFilterControlSwitchShow:function(){return"Показать панель инструментов"}},r.default.extend(r.default.fn.bootstrapTable.defaults,r.default.fn.bootstrapTable.locales["ru-RU"])}));
