Vue.config.devtools = true;
var userHomeDataSample = {
    articleListData: [
        {
            title: "Test Title 1",
            source: "Test Source 1",
            redir: "https://www.google.com/"
        },
        {
            title: "Test Title 2",
            source: "Test Source 2",
            redir: "https://www.bing.com/"
        },
    ]
};

var userHomeData = JSON.parse(document.getElementById('user-home-data').textContent);
console.log(userHomeDataSample)
console.log(userHomeData)

Vue.component('article-item', {
    delimiters: ['[[', ']]'],
    props: {
        articleTitle: String,
        articleSource: String,
        articleRedirLink: String
    },
    template: `
    <div class="article-item">
            <a :href="articleRedirLink">
                <article class="article_block">
                    [[  articleTitle  ]] -- [[ articleSource ]]
                </article>
            </a>
        </div>
    `,
    computed: {

    },
    methods: {

    }
});

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: function () {
        return {
            userHomeData: userHomeData
        }
    },
    computed: {
        articles: function () {
            return this.userHomeData.articleListData;
        }
    },
});