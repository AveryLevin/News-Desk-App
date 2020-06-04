var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        test: 'working!',
        tag: ''
    },
    methods: {
        updateValue: function(newName) {
            this.tag = newName;
        }
    }
})