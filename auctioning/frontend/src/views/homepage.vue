<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <div style="width:23vw; position: absolute; top: 1vw; left:0vw; height:auto">
        <div class='shadow  text-left m-4 p-3 bg-sucess' style="width:23vw;">
            <div style='font-size: 2vw;' class='h4 mb-4'>
                Profile
            </div>
            <img :src="'src/assets' + this.profile.proimage" style="width:10vw; height: 10vw;" />
            <p style='font-size: 1.25vw;' class='text-left mt-5 mb-2 me-3'> Welcome, {{ profile.newusername }} </p>
            <p style='font-size: 1.25vw;' class='mb-2 me-3'>Email: {{ profile.email }} </p>
            <p style='font-size: 1.25vw;' class='mb-2 me-3'>Date of Birth: {{ profile.birth }} </p>


        </div>
        <div class='shadow  text-center m-4 pt-20 p-3 bg-sucess' style="width:23vw; ">
            <p style='font-size: 1.25vw;'> Something wrong with your details ?</p>
            <router-link to="/Profile"
                style="font-size: 1vw; color: white; border-radius: 8px;padding-left: 3vw; padding-right: 3vw; "
                class="  bg-danger ">Edit</router-link>
        </div>
    </div>
    <div style="width:auto; position: absolute; top: 1vw; left:27vw; height:100%">
        <div class="input-group rounded">
            <input v-model="product" style="width:38vw;" type="search" class="form-control rounded"
                placeholder="Search a auction" aria-label="Search" aria-describedby="search-addon" />
            <button @click="searchproducts()" type="button" class="btn btn-outline-primary">search</button>
        </div>
        <ul class="list-group mt-3">
            <li @click="this.$router.push({ name: 'Auction', params: { id: sproduct.id } })" class="list-group-item"
                v-for=" sproduct in products">
                {{ sproduct.title }}
                <ul>
                    <li style="list-style-type: none; text-align: left;">Description: {{ sproduct.description }}</li>
                    <li style="list-style-type: none; text-align: left;">Price: {{ sproduct.price }}</li>
                </ul>
            </li>
        </ul>
    </div>
    <div style="width:auto; position: absolute; top: 1vw; left:73vw; height:100%">
        <div>
            <button @click="logout()" style="float: right; margin-right:2vw ;" type="button" class="btn btn-warning">Log
                Out</button>
        </div>
        <div class='shadow  text-center m-4 mt-5 pt-20 p-3 bg-sucess' style="width:23vw; ">
            <p style='font-size: 1.25vw;'>Create a new auction fast and easy </p>
            <router-link to="/Upload"
                style="font-size: 1vw; color: white; border-radius: 8px;padding-left: 3vw; padding-right: 3vw; "
                class="  bg-danger " type="submit">Create</router-link>
        </div>
    </div>
</template>
    
<script>

export default {
    data() {
        return {
            profile: {
                newusername: '',
                email: '',
                birth: '',
                proimage: '',
            },
            products: [],
            user: '',
            product: '',
            sproduct: '',
            id: '',
        }
    },
    methods: {
        async fetchProfile() {
            let response = await fetch(
                "http://localhost:8000/api/profile",
                {
                    method: 'GET',
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                });
            let data = await response.json()
            this.profile = data.profile
        },

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
            const response = await fetch("http://localhost:8000/api/productsearch", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                method: 'POST',
                headers: { "Content-Type": "application/json", "X-CSRFToken": this.getCookie("csrftoken") },
                body: JSON.stringify({ query: this.product })
            });
            let data = await response.json();
            this.products = data.products


        },

        async logout() {
            let response = await fetch(
                "http://localhost:8000/api/logout",
                {
                    method: 'GET',
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                });
            let data = await response.json()
            window.location.href = data.return


        },
    },
    beforeMount() {
        this.fetchProfile()
        this.searchproducts()
    },
    mounted() {
    },
}
</script>