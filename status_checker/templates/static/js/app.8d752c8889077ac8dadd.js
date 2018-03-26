webpackJsonp([1],{0:function(t,s){},Ba62:function(t,s){},NHnr:function(t,s,e){"use strict";Object.defineProperty(s,"__esModule",{value:!0});var o=e("7+uW"),a={name:"HelloWorld",data:function(){return{statusServiceUrl:location.protocol+"//"+location.hostname,refreshInterval:6e4,entries:[],items:[],logsDialog:!1,logsDialogTitle:"",timer:null,pythonVersion:"-"}},created:function(){this.fetchStatus(),this.startAutoRefresh(),this.getPythonVersion()},filters:{codeToColor:function(t){return 200===t?"status-green":0==t?"status-red":"status-orange"},codeToText:function(t){return 200===t?"Looks good!":0==t?"Appears to be dead...":"Is broken. Returns "+t}},methods:{startAutoRefresh:function(){this.timer=setInterval(function(){this.fetchStatus("")}.bind(this),this.refreshInterval)},fetchStatus:function(t){var s=this;this.entries.forEach(function(t){t.refreshed=!1}.bind(this)),this.$http.get(this.statusServiceUrl+"/get_status").then(function(e){var o=JSON.parse(e.bodyText);o.forEach(function(s){""!=t&&s.target_id!=t||(s.refreshed=!0)}.bind(s)),s.entries=o},function(t){})},updateStatus:function(t){var s=this;clearInterval(this.timer),this.$http.get(this.statusServiceUrl+"/update_status"+(""!=t?"/"+t:"")).then(function(e){s.fetchStatus(t),s.startAutoRefresh()},function(t){})},fetchLogs:function(t){var s=this;this.$http.get(this.statusServiceUrl+"/get_logs"+(""!=t?"/"+t:"")).then(function(e){s.items=JSON.parse(e.bodyText),s.logsDialog=!0,""==t?s.logsDialogTitle="All logs":s.items.length>0?s.logsDialogTitle=s.items[0].name+" logs":s.logsDialogTitle="No logs"},function(t){})},getPythonVersion:function(t){var s=this;this.$http.get(this.statusServiceUrl+"/python_version").then(function(t){s.pythonVersion=t.bodyText},function(t){})}}},i={render:function(){var t=this,s=t.$createElement,e=t._self._c||s;return e("v-app",[e("h1",[t._v("Is stuff ok?")]),t._v(" "),e("h3",[t._v("WebStatusMonitoring")]),t._v(" "),e("h4",[t._v("Running on Python "+t._s(t.pythonVersion))]),t._v(" "),e("v-container",{attrs:{"grid-list-md":""}},[e("v-layout",{attrs:{row:"",wrap:""}},t._l(t.entries,function(s){return e("v-flex",{key:s.target_id,attrs:{lg3:"",md4:"",sm6:"",xs12:""}},[e("v-card",{class:{fadeAnimation:s.refreshed},attrs:{"text-xs-center":"",color:t._f("codeToColor")(s.code)}},[e("v-card-text",{staticClass:"title"},[e("b",[t._v(t._s(s.name))])]),t._v(" "),e("v-card-text",[e("p",[t._v("Status: "+t._s(t._f("codeToText")(s.code)))]),t._v(" "),e("p",[t._v("Last check: "+t._s(s.checked))])]),t._v(" "),e("v-card-actions",[e("div",{staticClass:"margin-auto"},[e("v-tooltip",{attrs:{bottom:""}},[e("v-btn",{staticClass:"blue-button",attrs:{slot:"activator",dark:"",fab:"",small:"",href:s.url},slot:"activator"},[e("v-icon",[t._v("open_in_new")])],1),t._v(" "),e("span",[t._v("Open "+t._s(s.name))])],1),t._v(" "),e("v-tooltip",{attrs:{bottom:""}},[e("v-btn",{staticClass:"blue-button",attrs:{slot:"activator",dark:"",fab:"",small:""},on:{click:function(e){t.updateStatus(s.target_id)}},slot:"activator"},[e("v-icon",[t._v("refresh")])],1),t._v(" "),e("span",[t._v("Check status of "+t._s(s.name))])],1),t._v(" "),e("v-tooltip",{attrs:{bottom:""}},[e("v-btn",{staticClass:"blue-button",attrs:{slot:"activator",dark:"",fab:"",small:""},on:{click:function(e){e.stopPropagation(),t.fetchLogs(s.target_id)}},slot:"activator"},[e("v-icon",[t._v("assignment")])],1),t._v(" "),e("span",[t._v("Show logs of "+t._s(s.name))])],1)],1)])],1)],1)})),t._v(" "),e("v-dialog",{attrs:{scrollable:"","max-width":"400px"},model:{value:t.logsDialog,callback:function(s){t.logsDialog=s},expression:"logsDialog"}},[e("v-card",[e("v-card-title",{staticClass:"title"},[t._v(t._s(this.logsDialogTitle))]),t._v(" "),e("v-divider"),t._v(" "),e("v-card-text",[e("v-list",{attrs:{"three-line":""}},[t._l(this.items,function(s,o){return[e("v-list-tile",{on:{click:function(t){}}},[e("v-list-tile-content",[e("v-list-tile-title",[e("div",{staticClass:"status-code",class:t._f("codeToColor")(s.code)},[t._v(t._s(s.code))]),t._v(" "+t._s(s.name))]),t._v(" "),e("v-list-tile-sub-title",[t._v("Title: "+t._s(s.output_title))]),t._v(" "),e("v-list-tile-sub-title",[t._v(t._s(s.date)+" "),e("a",{attrs:{href:s.url}},[t._v("Link")])])],1)],1),t._v(" "),o+1<t.items.length?e("v-divider",{key:o}):t._e()]})],2)],1),t._v(" "),e("v-divider"),t._v(" "),e("v-card-actions",[e("v-btn",{staticClass:"blue-button margin-auto",attrs:{dark:"",fab:"",small:""},on:{click:function(s){s.stopPropagation(),t.logsDialog=!1}}},[e("v-icon",[t._v("check")])],1)],1)],1)],1),t._v(" "),e("v-tooltip",{attrs:{bottom:""}},[e("v-btn",{staticClass:"blue-button",attrs:{slot:"activator",dark:"",fab:"",small:""},on:{click:function(s){t.updateStatus("")}},slot:"activator"},[e("v-icon",[t._v("refresh")])],1),t._v(" "),e("span",[t._v("Check status of all services")])],1),t._v(" "),e("v-tooltip",{attrs:{bottom:""}},[e("v-btn",{staticClass:"blue-button",attrs:{slot:"activator",dark:"",fab:"",small:""},on:{click:function(s){t.fetchLogs("")}},slot:"activator"},[e("v-icon",[t._v("assignment")])],1),t._v(" "),e("span",[t._v("Show all logs")])],1)],1)],1)},staticRenderFns:[]};var n={name:"App",components:{HelloWorld:e("VU/8")(a,i,!1,function(t){e("wC7P")},null,null).exports}},r={render:function(){var t=this.$createElement,s=this._self._c||t;return s("div",{attrs:{id:"app"}},[s("HelloWorld")],1)},staticRenderFns:[]};var l=e("VU/8")(n,r,!1,function(t){e("Ba62")},null,null).exports,c=e("8+8L"),v=e("3EgV"),u=e.n(v);o.a.config.productionTip=!1,o.a.use(c.a),o.a.use(u.a),new o.a({el:"#app",components:{App:l},template:"<App/>"})},wC7P:function(t,s){}},["NHnr"]);
//# sourceMappingURL=app.8d752c8889077ac8dadd.js.map