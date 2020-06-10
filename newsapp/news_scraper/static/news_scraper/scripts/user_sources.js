Vue.config.devtools = true;
var rootURL = "http://192.168.1.158:8000/news"

var userSourcesDataSamples = {
    currentSources: [
        { name: "Ex1" },
        { name: "Ex.2" },
        { name: "Ex.3" },
    ],
    additionalSources: [
        { name: "Ex.4" },
        { name: "Ex.5" },
        { name: "Ex.6" },
    ]
};


var userSourcesData = JSON.parse(document.getElementById('user-source-data').textContent);
console.log(userSourcesData);

Vue.component('current-source-item', {
    delimiters: ['[[', ']]'],
    data: function () {
        return {
            classType: "source-item-light",
            postTo: rootURL + "/user_home/sources"
        };
    },
    props: {
        name: String,
        source: Object
    },
    template: `
    <li :class="classType">
                <div class=left-side>[[ name ]]</div>
                
                <button 
                @click="removeSource" 
                @mouseover="makeItemDark"
                @mouseleave="makeItemLight"
                id="rm_src" class="edit-source">Remove Source</button>
            </li>
    `,
    computed: {

    },
    methods: {
        makeItemDark: function () {
            this.classType = "source-item-dark";
        },
        makeItemLight: function () {
            this.classType = "source-item-light";
        },
        removeSource: function () {
            console.log("Attempting POST Request to " + this.postTo);
            let postData = JSON.stringify({
                action: "Remove Source",
                name: this.name
            });
            var self = this;
            fetch(this.postTo, {
                method: 'post',
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: postData,

            }).then(
                function (response) {
                    if (response.status != 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                            response.status);
                        return;
                    }

                    //check response data
                    response.json().then(function (data) {

                        temp = data.sourceData;
                        userSourcesData = temp;
                        console.log("sending:");
                        console.log(userSourcesData);
                        self.$emit('sources-changed', userSourcesData);
                    });
                }
            ).catch(function (err) {
                console.log('Fetch Error :-S', err);
            });

        }
    }
})

Vue.component('additional-source-item', {
    delimiters: ['[[', ']]'],
    data: function () {
        return {
            classType: "source-item-light",
            postTo: rootURL + "/user_home/sources"
        };
    },
    props: {
        name: String,
        source: Object
    },
    template: `
    <li :class="classType">
                <div class=left-side>[[ name ]]</div>
                <button 
                @click="removeSource" 
                @mouseover="makeItemDark"
                @mouseleave="makeItemLight"
                id="rm_src" class="edit-source">Add Source</button>
    </li>
    `,
    computed: {

    },
    methods: {
        makeItemDark: function () {
            this.classType = "source-item-dark";
        },
        makeItemLight: function () {
            this.classType = "source-item-light";
        },
        removeSource: function () {
            console.log("Attempting POST Request to " + this.postTo);
            let postData = JSON.stringify({
                action: "Add Source",
                name: this.name
            });
            var self = this;
            fetch(this.postTo, {
                method: 'post',
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: postData,

            }).then(
                function (response) {
                    if (response.status != 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                            response.status);
                        return;
                    }

                    //check response data
                    response.json().then(function (data) {

                        temp = data.sourceData;
                        userSourcesData = temp;
                        console.log("sending:");
                        console.log(userSourcesData);
                        self.$emit('sources-changed', userSourcesData);
                    });
                }
            ).catch(function (err) {
                console.log('Fetch Error :-S', err);
            });

        }
    }
})


var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueinst',
    data: {
        userSourcesData: userSourcesData
    },
    computed: {
        currentSources: function () {
            return this.userSourcesData.currentSources;
        },
        additionalSources: function () {
            return this.userSourcesData.additionalSources;
        },
    },
    methods: {
        updateSources: function (newData) {
            console.log("updating data:");
            console.log(newData);
            this.userSourcesData = newData;
        }
    },
    template: `
    <div>
        <ul class="source-list">
            <h4>Your current sources:</h4>
            <current-source-item 
            v-for="source in this.currentSources" 
            v-bind:name="source.name"
            v-on:sources-changed="updateSources">
            </current-source-item>
        </ul>

        <ul class="source-list">
            <h4>Other availabe sources:</h4>
            <additional-source-item 
            v-for="source in this.additionalSources" 
            v-bind:name="source.name"
            v-on:sources-changed="updateSources">
            </additional-source-item>
        </ul>
    </div>

    `,
});
