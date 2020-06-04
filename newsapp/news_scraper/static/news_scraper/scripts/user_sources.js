
var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        test: 'working!',
        src: ''
    },
    methods: {
        updateValue: function(newName) {
            this.src = newName;
        }
    }
})