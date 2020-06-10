Vue.config.devtools = true;
var rootURL = "http://127.0.0.1:8000/news"

var userSourcesDataSamples = {
    currentSources: [
        { name: "Ex.1" },
        { name: "Ex.2" },
        { name: "Ex.3" },
    ],
    additionalSources: [
        { name: "Ex.4" },
        { name: "Ex.5" },
        { name: "Ex.6" },
    ]
};

Vue.component('current-source-item', {
    delimiters: ['[[', ']]'],
    data: function () {
        return {
            classType: "source-item-light",
            postTo: rootURL + "/user_home/sources"
        }
    },
    props: {
        name: String
    },
    template: `
    <li :class="classType">
                <div class=left-side>[[ name ]]</div>
                
                <button 
                @click="newName" 
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
        newName: function () {
            console.log("Attempting POST Request to " + this.postTo);
            let postData = JSON.stringify(this.data());
            fetch(this.postTo, {
                method: 'post',
                credentials: "same-origin",
                headers: {
                    "X-CSRFTOKEN": csrftoken,
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
                        console.log(data);
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
            classType: "source-item-light"
        }
    },
    props: {
        name: String
    },
    template: `
    <li :class="classType">
                <div class=left-side>[[ name ]]</div>
                
                <div @click="" id="rm_src" class="edit-source">Remove Source</div>
            </li>
    `,
    computed: {

    },
    methods: {
        makeItemDark: function () {
            this.classType = "article-item-dark";
        },
        makeItemLight: function () {
            this.classType = "article-item-light";
        }
    }
})

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: function () {
        return {
            userSourcesData: userSourcesDataSamples
        }
    },
    computed: {
        currentSources: function () {
            return this.userSourcesData.currentSources;
        },
        additionalSources: function () {
            return this.userSourcesData.additionalSources;
        },
    },
});
console.log(csrftoken)