<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <div style="width:30%; position: absolute; top: 1vw; left:0vw; height:100%">
        <img :src="'../src/assets' + products1.image"
            style="width:100%; height: auto; margin-top: 15%; margin-left: 3%;" />
    </div>
    <div style="width:40%; position: absolute; top: 1vw; left:40%; height:100%">
        <h1> {{ products1.title }} </h1>
        <p style="margin-top: 4%; font-size: 1.5vw">Description</p>
        <p style="font-size: 1.25vw">{{ products1.description }}</p>
        <p style="margin-top: 10%; font-size: 1.5vw">Price</p>
        <p style="font-size: 1.2vw">{{ products1.price }} pounds</p>
        <p style="margin-top: 5%; font-size: 1.5vw">Bid ends at</p>
        <p type="date" style="font-size: 1.2vw">{{ products1.bidend }}</p>
        <p style="margin-top: 5%; font-size: 1.5vw">User winning: {{ products1.winbid }}</p>
        <input v-model="bid" style="margin-top: 5%; width: 6vw; height: 3vw; font-size: 1.25vw; " type="number"
            id="quantity" name="quantity" min="1">
        <button @click="makebid(), clearFields()"
            style=" margin-left: 3vw; background-color: red; font-size: 1vw; color: white; border-radius: 8px; padding-top: 0.5vw; padding-bottom: 0.5vw; padding-left: 3vw; padding-right: 3vw; "
            type="submit">Place Bid</button>
        <p style="margin-top: 5%; font-size: 1.5vw; color: red;">{{ products1.bidstate }}</p>
    </div>
    <div style="width:28%; position: absolute; top: 1vw; left:70%; height:100%">
        <h2>Questions</h2>
        <ul class="list-group mt-3">
            <li class="list-group-item" v-for=" squestions in questions">
                <ul>
                    <button style="float: right; width: 5vw; height: 1.5vw;font-size: 0.5vw;" class="btn float-right"
                        id="answer" type="button" @click="addanswer(squestions), clearFieldanswer()">submit</button>
                    <li style="list-style-type: none; text-align: left;">Question: {{ squestions.question }}</li>
                    <li style="list-style-type: none; text-align: left;">Answer: <input v-model="answeruser"
                            style="margin-top: 5%; width: 15vw; height: 1.5vw; font-size: 1.1vw; " type="text"
                            id="newquestion" :placeholder=squestions.answer></li>
                </ul>
            </li>
        </ul>
        <div class="input-group rounded">
            <input v-model="questionuser" style="margin-top: 5%; width: 20vw; height: 1.5vw; font-size: 1.1vw; "
                class="form-control rounded" type="text" id="newquestion" placeholder="Ask a question">
            <button @click="uploadquestion()" style="height: 1.5vw; margin-top: 5%; font-size: 0.5vw; " type="button"
                class="btn btn-outline-primary">Post</button>
        </div>
    </div>
</template>



<script>
export default {
    data() {
        return {
            profiles: [],
            // products: [],
            products1: {
                'id': '',
                'title': '',
                'description': '',
                'price': '',
                'bidend': '',
                'winbid': '',
                'bidstate': '',
                'image': '',
            },
            questions: [],
            user: '',
            email: '',
            product: '',
            sproduct: '',
            id: '',
            bid: '',
            dateformat: "",
            questionuser: '',
            answeruser: '',
        }
    },
    methods: {


        getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },


        async searchproducts() {
            const response = await fetch("http://localhost:8000/api/product", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                method: 'POST',
                headers: { "Content-Type": "application/json", "X-CSRFToken": this.getCookie("csrftoken") },
                body: JSON.stringify({ object: this.$route.params.id })
            });
            let data = await response.json();
            console.log(data.products)
            this.products1 = data.products[0]

        },

        async searchquestion() {
            const response = await fetch("http://localhost:8000/api/questionsearch", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                method: 'POST',
                headers: { "Content-Type": "application/json", "X-CSRFToken": this.getCookie("csrftoken") },
                body: JSON.stringify({ object: this.$route.params.id })
            });
            let data = await response.json();
            this.questions = data.questions


        },

        async makebid() {
            const response = await fetch("http://localhost:8000/api/bidview", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                method: 'POST',
                headers: { "Content-Type": "application/json", "X-CSRFToken": this.getCookie("csrftoken") },
                body: JSON.stringify({ object: this.$route.params.id, bid: this.bid })
            });
            let data = await response.json();
            console.log(data.products[0])
            this.products1 = data.products[0]


        },
        async uploadquestion() {
            const response = await fetch("http://localhost:8000/api/postquestion", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                method: 'POST',
                headers: { "Content-Type": "application/json", "X-CSRFToken": this.getCookie("csrftoken") },
                body: JSON.stringify({ object: this.$route.params.id, question: this.questionuser })
            });
            let data = await response.json();
            this.questions = data.questions


        },
        async addanswer(answered) {
            const response = await fetch("http://localhost:8000/api/postanswer", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                method: 'POST',
                headers: { "Content-Type": "application/json", "X-CSRFToken": this.getCookie("csrftoken") },
                body: JSON.stringify({ object: this.$route.params.id, answer: this.answeruser, id: answered.id })
            });
            let data = await response.json();
            this.questions = data.questions


        },
        async clearFieldanswer() {
            this.answeruser = "";
            document.getElementById("answer").value = "";
        },

        async clearFields() {
            this.bid = 0;
            document.getElementById("quantity").value = 0;
        },
    },
    beforeMount() {
        this.searchproducts()
        this.searchquestion()
    },
    mounted() {
    },
}

</script>