

var item = new Vue({
    delimiters: ['[[', ']]'],
    el: context_var,
    data: {
        class: "article-item-light"
    },
    methods:{
        makeDark: function() {
            console.log("test")
            this.class = "article-item-dark"
        }
    }

})