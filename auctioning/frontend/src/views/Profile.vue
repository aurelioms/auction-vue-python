<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <div>
        <div v-if="editable" class="container">
            <form @submit="updateProfile" method="POST" enctype="multipart/form-data">
                <div class="row m-3">
                    <div class="text-center">
                        Email
                        <div class="text-center">
                            <input style="margin: 0 auto;" class="form-control w-50 p-2" v-model="user.email">
                        </div>
                    </div>
                </div>
                <div class="row m-3">
                    <div class="text-center">
                        Birth(yyyy-mm-dd)
                        <div>
                            <input style="margin: 0 auto;" class="form-control w-50 p-2" v-model="user.birth">
                        </div>
                    </div>
                </div>
                <div class="row m-3">
                    <div class="text-center">
                        Image
                        <div>
                            <input @change="updateImage" type="file">
                        </div>
                    </div>
                </div>
                <div class="text-center">
                    <button class="btn btn-primary m-2" type="submit">SUBMIT</button>
                    <button @click="setEditable" class="btn btn-danger m-2">CANCEL</button>
                </div>
            </form>
        </div>
        <div v-else class="container">
            <div class="row m-3">
                <div class="text-center">
                    Email
                    <div class="text-center">
                        <p style="margin: 0 auto;" class="col-sm border rounded border-primary p-2 w-50">
                            {{ user.email }}
                        </p>
                    </div>
                </div>
            </div>
            <div class="row m-3">
                <div class="text-center">
                    Birth(yyyy-mm-dd)
                    <p style="margin: 0 auto;" class="col-sm border rounded border-primary p-2 w-50">
                        {{ user.birth }}
                    </p>
                </div>
            </div>
            <div class="row m-3">
                <p class="text-center">Profile picture</p>
                <div style="margin: auto; width: 30%; height: 30%;" class="border border-primary rounded text-center">
                    <img class="p-3" style="width: 50%; height: 50%;" :src="'src/assets' + this.user.proimage" />
                </div>
            </div>
            <div class="row m-3">
                <div class="text-center">
                    <button @click="setEditable" class="btn m-2 btn-info">EDIT</button>
                    <button @click="homepage" class="btn m-2 btn-success">GO BACK</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            user: {
                email: '',
                proimage: '',
                birth: ''
            },
            newImage: '',
            editable: false,
        }
    },
    methods: {
        homepage() {
            window.location.href = 'http://localhost:5173'
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
        updateImage(e) {
            this.newImage = e.target.files[0]
        },
        setEditable() {
            this.editable = !this.editable
        },

        async fetchProfile() {
            const response = await fetch("http://localhost:8000/api/profile", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer",
                method: 'GET',
                headers: { "Content-Type": "application/json", "X-CSRFToken": this.getCookie("csrftoken") },
            })
            const data = await response.json()
            console.log(data)
            this.user = data.profile
        },

        async updateProfile(e) {
            try {
                e.preventDefault()
                const formData = new FormData();
                formData.append('email', this.user.email)
                formData.append('proimage', this.newImage)
                formData.append('birth', this.user.birth)
                fetch("http://localhost:8000/api/profile", {
                    method: "POST",
                    body: formData,
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    headers: { "X-CSRFToken": this.getCookie("csrftoken") },
                }).then(res => res.json()).then(data => console.log(data))
                this.editable = !this.editable
                this.homepage()
            }
            catch (error) {
                alert("Failed to update profile")
            }
        },
    },

    created: function () {
        this.fetchProfile();
    },
}
</script>