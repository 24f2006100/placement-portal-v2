<template>

<div class="container">

    <div class="auth-card">

        <h1>Placement Portal</h1>
        <h3>Campus Recruitment System</h3>

        <form @submit.prevent="login">

            <div class="form-group">
                <label>Email</label>
                <input
                    type="email"
                    placeholder="Enter Email"
                    v-model="email"
                    required
                >
            </div>

            <div class="form-group">
                <label>Password</label>
                <input
                    type="password"
                    placeholder="Enter Password"
                    v-model="password"
                    required
                >
            </div>

            <div class="form-group">
                <label>Login As</label>

                <select v-model="role">

                    <option value="student">Student</option>

                    <option value="company">Company</option>

                    <option value="admin">Admin</option>

                </select>

            </div>

            <button class="btn">
                Login
            </button>

        </form>

        <br>

        <p>{{ message }}</p>

        <div class="links">

            <router-link to="/student/register">
                Student Register
            </router-link>

            <router-link to="/company/register">
                Company Register
            </router-link>

        </div>

    </div>

</div>

</template>

<script setup>

import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const email = ref("")
const password = ref("")
const role = ref("student")
const message = ref("")

const login = async () => {

    try{

        const response = await api.post("/login",{

            email:email.value,
            password:password.value,
            role:role.value

        })

        localStorage.setItem("token",response.data.access_token)
        localStorage.setItem("role",response.data.role)
        localStorage.setItem("full_name", response.data.full_name)

        if(response.data.role==="admin"){
            router.push("/admin/dashboard")
        }

        else if(response.data.role==="student"){
            router.push("/student/dashboard")
        }

        else{
            router.push("/company/dashboard")
        }

    }

    catch(error){

        message.value=error.response.data.message

    }

}

</script>