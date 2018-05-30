<template>
  <v-app>
    <h1>Status Checker</h1>
    <h3><a class="gray" href="https://github.com/justinasr/WebStatusMonitoring">WebStatusMonitoring</a></h3>
    <h4>Running on Python {{ pythonVersion }}</h4>
    <v-container grid-list-md>
      <v-layout row wrap>
        <v-flex lg3 md4 sm6 xs12 v-for="(entry, index) in entries" :key="entry.target_id">
          <v-card v-bind:class="'elevation-10 ' + (entry.disabled ? 'disabled':'enabled')" text-xs-center :color="entry.code | codeToColor">
            <v-card-text class="title"><b>{{ entry.name }}</b></v-card-text>
            <v-card-text v-if="!entry.disabled">
              <p>Status: {{ entry.code | codeToText }}</p>
              <p v-if="entry.code != -1">Last check: {{ entry.checked }}</p>
              <p>Title: {{ entry.output_title }}</p>
            </v-card-text>
            <v-card-text v-if="entry.disabled">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </v-card-text>
            <v-card-actions>
              <div class="margin-auto">
                <v-tooltip bottom v-if="entry.display_url">
                  <v-btn slot="activator" dark fab small class="blue-button elevation-3" :href="entry.display_url" target="_blank"><v-icon>open_in_new</v-icon></v-btn>
                  <span>Open {{ entry.name }}</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <v-btn slot="activator" dark fab small class="blue-button elevation-3" v-on:click="updateStatus(index)"><v-icon>refresh</v-icon></v-btn>
                  <span>Check status of {{ entry.name }}</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <v-btn slot="activator" dark fab small class="blue-button elevation-3" @click.stop="fetchLogs(entry.target_id)"><v-icon>assignment</v-icon></v-btn>
                  <span>Show logs of {{ entry.name }}</span>
                </v-tooltip>
              </div>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>

      <v-dialog scrollable v-model="logsDialog" max-width="400px">
        <v-card>
          <v-card-title class="title">{{ this.logsDialogTitle }}</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-list three-line>
              <template v-for="(item, index) in this.items">
                <v-list-tile  @click="">
                  <v-list-tile-content>
                    <v-list-tile-title><div class="status-code" :class="item.code | codeToColor ">{{ item.code }}</div> {{ item.name }}</v-list-tile-title>
                    <v-list-tile-sub-title>Title: {{ item.output_title }}</v-list-tile-sub-title>
                    <v-list-tile-sub-title>Check: {{ item.checked }}</v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider v-if="index + 1 < items.length" :key="index"></v-divider>
              </template>
            </v-list>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn dark fab small class="blue-button margin-auto" @click.stop="logsDialog=false"><v-icon>check</v-icon></v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-tooltip bottom>
        <v-btn slot="activator" dark fab small class="blue-button" v-on:click="updateAll()"><v-icon>refresh</v-icon></v-btn>
        <span>Check status of all services</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn slot="activator" dark fab small class="blue-button" v-on:click="fetchLogs()"><v-icon>assignment</v-icon></v-btn>
        <span>Show all logs</span>
      </v-tooltip>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: 'MainComponent',
  data () {
    return {
      statusServiceUrl: location.protocol + '//' + location.hostname + (location.pathname != '/' ? location.pathname : ''),
      refreshInterval: 60000,
      entries: null,
      items: [],
      logsDialog: false,
      logsDialogTitle: '',
      timer: null,
      pythonVersion: '-'
    }
  },
  created () {
    this.fetchStatus()
    this.startAutoRefresh()
    this.getPythonVersion()
  },
  filters: {
    codeToColor (code) {
      if (code === 200) {
        return "status-green"
      } else if (code == 0) {
        return "status-red"
      } else if (code == -1) {
        return "status-gray"
      } else {
        return "status-orange"
      }
    },
    codeToText (code) {
      if (code === 200) {
        return "Looks good!"
      } else if (code == 0) {
        return "Appears to be dead..."
      } else if (code == -1) {
        return "Hasn't been checked yet."
      } else {
        return "Is broken. Returns " + code
      }
    }
  },
  methods: {
    startAutoRefresh: function () {
      clearInterval(this.timer)

      this.timer = setInterval(function() {
        this.fetchStatus()
      }.bind(this), this.refreshInterval);
    },
    async fetchStatus (targetId) {
      const response = await this.$http.get(this.statusServiceUrl + '/get_status')

      const parsed = JSON.parse(response.bodyText)
      parsed.forEach(entry => {
        entry.disabled = (targetId === entry.target_id)

        setTimeout(() => {
          entry.disabled = false
        }, Math.random() * 1000)
      })

      this.$set(this, 'entries', parsed)
    },
    async updateAll () {
      this.startAutoRefresh()
      this.entries.forEach(function (value) {
        value.disabled = true
      })

      await this.$http.get(this.statusServiceUrl + '/update_status')
      this.fetchStatus()
    },
    async updateStatus (index) {
      const targetId = this.entries[index].target_id
      this.entries[index].disabled = true

      await this.$http.get(this.statusServiceUrl + '/update_status/' + targetId)
      this.fetchStatus(targetId)
    },
    fetchLogs: function (targetId) {
      this.$http.get(this.statusServiceUrl + '/get_logs' + (targetId != undefined ? '/' + targetId : '')).then(response => {
        this.items = JSON.parse(response.bodyText)
        this.logsDialog = true
        if (targetId == undefined) {
          this.logsDialogTitle = 'All logs'
        } else {
          if (this.items.length > 0) {
            this.logsDialogTitle = this.items[0].name + ' logs'
          } else {
            this.logsDialogTitle = 'No logs'
          }
        }
      }, response => {
      })
    },
    getPythonVersion: function (targetId) {
      this.$http.get(this.statusServiceUrl + '/python_version').then(response => {
        this.pythonVersion = response.bodyText
      }, response => {
      })
    },
  }
}
</script>

<style>
h1 {
  font-size: 3rem;
}

.status-green {
  background-color: #87D37C !important;
}

.status-orange {
  background-color: #F5D76E !important;
}

.status-red {
  background-color: #EC644B !important;
}

.status-gray {
  background-color: #DDDDDD !important;
}

.blue-button {
  background-color: #007bff !important;
}

.margin-auto {
  margin: auto !important;
}

.status-code {
  display: inline-block;
  width: 40px;
  text-align: center;
}

.card {
  height: 100% !important;
  padding-bottom: 64px !important;
}

.card__actions {
  width: 100% !important;
  position: absolute !important;
  bottom: 8px !important;
}

.card__text p {
  margin-bottom: 2px !important;
}

.card.disabled { 
  opacity: 0.4;
}

.card.enabled {
  -webkit-animation: fadein 1.5s; /* Safari, Chrome and Opera > 12.1 */
     -moz-animation: fadein 1.5s; /* Firefox < 16 */
      -ms-animation: fadein 1.5s; /* Internet Explorer */
       -o-animation: fadein 1.5s; /* Opera < 12.1 */
          animation: fadein 1.5s;
}

.gray {
  text-decoration: none;
  color: #2c3e50 !important;
}

.gray:hover {
  color: #2c3e50 !important;
}

@keyframes fadein {
    from { opacity: 0.4; }
    to   { opacity: 1; }
}

/* Firefox < 16 */
@-moz-keyframes fadein {
    from { opacity: 0.4; }
    to   { opacity: 1; }
}

/* Safari, Chrome and Opera > 12.1 */
@-webkit-keyframes fadein {
    from { opacity: 0.4; }
    to   { opacity: 1; }
}

/* Internet Explorer */
@-ms-keyframes fadein {
    from { opacity: 0.4; }
    to   { opacity: 1; }
}

/* Opera < 12.1 */
@-o-keyframes fadein {
    from { opacity: 0.4; }
    to   { opacity: 1; }
}

</style>
