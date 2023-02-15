<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <div>
        <div class="container">
            <form @submit="newProduct" method="POST" enctype="multipart/form-data">
                <div class="row m-3">
                    <div class="text-center">
                        Title
                        <div class="text-center">
                            <input style="margin: 0 auto;" class="form-control w-50 p-2" v-model="product.title">
                        </div>
                    </div>
                </div>
                <div class="row m-3">
                    <div class="text-center">
                        Price
                        <div>
                            <input style="margin: 0 auto;" class="form-control w-50 p-2" v-model="product.price">
                        </div>
                    </div>
                </div>
                <div class="row m-3">
                    <div class="text-center">
                        Description
                        <div>
                            <input style="margin: 0 auto;" class="form-control w-50 p-2" v-model="product.description">
                        </div>
                    </div>
                </div>
                <div class="row m-3">
                    <div class="text-center">
                        Image
                        <div>
                            <input style="margin: 0 auto;" @change="updateImage" type="file">
                        </div>
                    </div>
                </div>
                <div class=" row m-3">
                    <div class="text-center">
                        Bid end (yyyy-mm-dd)
                        <div>
                            <input style="margin: 0 auto;" class="form-control w-50 p-2" v-model="product.bidend">
                        </div>
                    </div>
                </div>
                <div class="text-center">
                    <button class="btn btn-primary m-2" type="submit">SUBMIT</button>
                </div>
            </form>
            <div class="text-center">
                <button @click="homepage" class="btn btn-success m-2">GO BACK</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            product: {
                title: '',
                price: '',
                description: '',
                image: '',
                bidend: '',
                winbid: '',
            },
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
        async newProduct(e) {
            try {
                e.preventDefault()
                const now = new Date()
                const d1 = new Date(this.product.bidend)
                if (d1 < now)
                    throw new Error()
                const formData = new FormData();
                formData.append('title', this.product.title)
                formData.append('price', this.product.price)
                formData.append('description', this.product.description)
                formData.append('image', this.product.image)
                formData.append('bidend', this.product.bidend)
                fetch("http://localhost:8000/api/upload", {
                    method: "POST",
                    body: formData,
                    credentials: "include",
                    mode: "cors",
                    referrerPolicy: "no-referrer",
                    headers: { "X-CSRFToken": this.getCookie("csrftoken") },
                }).then(res => res.json()).then(data => console.log(data))
                alert("Successfully added a product")
                window.location.href = 'http://localhost:5173'
            } catch (error) {
                alert("Error occurred, failed to add product. Please enter the correct details or retry")
            }
        },

        updateImage(e) {
            this.product.image = e.target.files[0]
        }
    }

}
</script>