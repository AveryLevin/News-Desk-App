
var userHomeData = {
    articleListData: [
        {
            articleTitle: "Test Title 1",
            articleSource: "Test Source 1",
            articleRedirLink: "https://www.google.com/"
        },
        {
            articleTitle: "Test Title 2",
            articleSource: "Test Source 2",
            articleRedirLink: "https://www.bing.com/"
        },
    ]
};

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