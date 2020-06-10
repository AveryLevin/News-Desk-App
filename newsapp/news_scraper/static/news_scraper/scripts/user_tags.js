Vue.config.devtools = true;
var rootURL = "http://127.0.0.1:8000/news"

var userTagsDataSamples = {
    userTags: [
        { name: "Ex1" },
        { name: "Ex.2" },
        { name: "Ex.3" },
    ],
    popularTags: [
        { name: "Ex.4" },
        { name: "Ex.5" },
        { name: "Ex.6" },
    ]
};

var userTagsData = JSON.parse(document.getElementById('user-tag-data').textContent);
console.log(userTagsData);

Vue.component('current-tag-item', {
    delimiters: ['[[', ']]'],
    data: function () {
        return {
            classType: "tag-item-light",
            postTo: rootURL + "/user_home/tags"
        };
    },
    props: {
        name: String,
        tag: Object
    },
    template: `
    <li :class="classType">
                <div class=left-side>[[ name ]]</div>
                
                <button 
                @click="removeTag" 
                @mouseover="makeItemDark"
                @mouseleave="makeItemLight"
                id="rm_src" class="edit-tag">Delete Tag</button>
            </li>
    `,
    computed: {

    },
    methods: {
        makeItemDark: function () {
            this.classType = "tag-item-dark";
        },
        makeItemLight: function () {
            this.classType = "tag-item-light";
        },
        removeTag: function () {
            console.log("Attempting POST Request to " + this.postTo);
            let postData = JSON.stringify({
                action: "Delete Tag",
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

                        temp = data.tagData;
                        userTagsData = temp;
                        console.log("sending:");
                        console.log(userTagsData);
                        self.$emit('tags-changed', userTagsData);
                    });
                }
            ).catch(function (err) {
                console.log('Fetch Error :-S', err);
            });

        }
    }
})

Vue.component('additional-tag-item', {
    delimiters: ['[[', ']]'],
    data: function () {
        return {
            classType: "tag-item-light",
            postTo: rootURL + "/user_home/tags"
        };
    },
    props: {
        name: String,
        tag: Object
    },
    template: `
    <li :class="classType">
                <div class=left-side>[[ name ]]</div>
                
                <button 
                @click="removeTag" 
                @mouseover="makeItemDark"
                @mouseleave="makeItemLight"
                id="rm_src" class="edit-tag">Add Tag</button>
            </li>
    `,
    computed: {

    },
    methods: {
        makeItemDark: function () {
            this.classType = "tag-item-dark";
        },
        makeItemLight: function () {
            this.classType = "tag-item-light";
        },
        removeTag: function () {
            console.log("Attempting POST Request to " + this.postTo);
            let postData = JSON.stringify({
                action: "Add Tag",
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

                        temp = data.tagData;
                        userTagsData = temp;
                        console.log("sending:");
                        console.log(userTagsData);
                        self.$emit('tags-changed', userTagsData);
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
        userTagsData: userTagsData
    },
    computed: {
        currentTags: function () {
            return this.userTagsData.userTags;
        },
        additionalTags: function () {
            return this.userTagsData.popularTags;
        },
    },
    methods: {
        updateTags: function (newData) {
            console.log("updating data:");
            console.log(newData);
            this.userTagsData = newData;
        }
    },
    template: `
    <div class="tags_list">
        <ul class="tags-list">
            <h4>Your current tags:</h4>
            <div class="hztl-line"></div>
            <current-tag-item 
            v-for="tag in this.currentTags" 
            v-bind:name="tag.name"
            v-on:tags-changed="updateTags">
            </current-tag-item>
        </ul>
        <br>
        
        <ul class="tags-list">
            <h4>Here are some trending tags:</h4>
            <div class="hztl-line"></div>
            <additional-tag-item 
            v-for="tag in this.additionalTags" 
            v-bind:name="tag.name"
            v-on:tags-changed="updateTags">
            </additional-tag-item>
        </ul>
    </div>

    `,
})