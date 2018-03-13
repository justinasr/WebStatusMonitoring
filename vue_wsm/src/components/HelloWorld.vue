<template>
  <v-app>
    <h1>Is stuff ok?</h1>
    <v-container grid-list-md>
      <v-layout row wrap>
        <v-flex lg3 md4 sm6 xs12 v-for="entry in entries" :key="entry.target_id">
          <v-card text-xs-center :color="entry.code | codeToColor ">
            <v-card-text class="title">{{ entry.name }}</v-card-text>
            <v-card-text class="px-0">
              <p>Status: {{ entry.code | codeToText }}</p>
              <p>Last check: {{ entry.checked }}</p>
            </v-card-text>
            <v-card-actions>
              <div class="margin-auto">
                <v-tooltip bottom>
                  <v-btn slot="activator" dark fab small class="blue-button" :href="entry.url"><v-icon>open_in_new</v-icon></v-btn>
                  <span>Open {{ entry.name }}</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <v-btn slot="activator" dark fab small class="blue-button" v-on:click="updeitas2(entry.target_id)"><v-icon>refresh</v-icon></v-btn>
                  <span>Check status of {{ entry.name }}</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <v-btn slot="activator" dark fab small class="blue-button" @click.stop="logai2(entry.target_id)"><v-icon>assignment</v-icon></v-btn>
                  <span>Show logs of {{ entry.name }}</span>
                </v-tooltip>
              </div>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>

      <v-dialog scrollable v-model="dialog3" max-width="400px">
        <v-card>
          <v-card-title class="title">{{ this.dialog3Title }}</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-list three-line>
              <template v-for="(item, index) in this.items">
                <v-list-tile  @click="">
                  <v-list-tile-content>
                    <v-list-tile-title><div class="status-code" :class="item.code | codeToColor ">{{ item.code }}</div> {{ item.name }}</v-list-tile-title>
                    <v-list-tile-sub-title>Title: {{ item.output_title }}</v-list-tile-sub-title>
                    <v-list-tile-sub-title>{{ item.date }} <a :href="item.url">{{ item.url }}</a></v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider v-if="index + 1 < items.length" :key="index"></v-divider>
              </template>
            </v-list>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn dark fab small class="blue-button margin-auto" @click.stop="dialog3=false"><v-icon>thumb_up</v-icon></v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-tooltip bottom>
        <v-btn slot="activator" dark fab small class="blue-button" v-on:click="updeitas"><v-icon>refresh</v-icon></v-btn>
        <span>Check status of all services</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn slot="activator" dark fab small class="blue-button" v-on:click="logai"><v-icon>assignment</v-icon></v-btn>
        <span>Show all logs</span>
      </v-tooltip>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      entries: [],
      items: [],
      dialog3: false,
      dialog3Title: ''
    }
  },
  created () {
    this.fetchas()
    setInterval(function() {
        this.fetchas()
    }.bind(this), 15000);
    
  },
  filters: {
    codeToColor (code) {
      if (code === 200) {
        return "status-green"
      } else if (code == 0) {
        return "status-red"
      } else {
        return "status-orange"
      }
    },
    codeToText (code) {
      if (code === 200) {
        return "Looks good!"
      } else if (code == 0) {
        return "Appears to be dead..."
      } else {
        return "Is broken. Returns " + code
      }
    }
  },
  methods: {
    fetchas: function () {
      this.$http.get('http://instance4:5000/get_status').then(response => {
        this.entries = JSON.parse(response.bodyText)
        console.log('fetchas')
      }, response => {
      })
    },
    updeitas2: function (target_id) {
      this.$http.get('http://instance4:5000/update_status/' + target_id).then(response => {
        this.fetchas()
      }, response => {
      })
    },
    updeitas: function () {
      this.$http.get('http://instance4:5000/update_status').then(response => {
        this.fetchas()
      }, response => {
      })
    },
    logai: function () {
      this.$http.get('http://instance4:5000/get_logs').then(response => {
        this.items = JSON.parse(response.bodyText)
        this.dialog3 = true
        this.dialog3Title = 'All logs'
      }, response => {
      })
    },
    logai2: function (target_id) {
      this.$http.get('http://instance4:5000/get_logs/' + target_id).then(response => {
        this.dialog3 = true
        this.items = JSON.parse(response.bodyText)
        this.entries.forEach(function (value) {
          if (value.target_id == target_id) {
            this.dialog3Title = value.name + ' logs'
          }
        }.bind(this))
      }, response => {
      })
    }
  }
}
</script>

<style>
.status-green {
  background-color: #87D37C !important;
}

.status-orange {
  background-color: #F5D76E !important;
}

.status-red {
  background-color: #EC644B !important;
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

</style>
