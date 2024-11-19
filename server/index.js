const express = require("express")
const mongoose = require('mongoose')
const cors = require('cors')
const UserModel = require('./models/User')

const app = express()
app.use(express.json())  //passes data from frontend to backend
app.use(cors())

mongoose.connect("mongodb://127.0.0.1:27017/User")  //paste connection string 

app.post("/login",(req,res) => {
    const {email,password} = req.body;
    UserModel.findOne({email: email})
    .then(user => {
        if(user) {
            if(user.password === password){
                res.json("Success")
            } else {
                res.json("the password is incorrect")
            } 
        } else {
            res.json("No record existed")
        }
    })
})

app.post('/signup',(req, res) => {    //request(data coming from frontend) and resp sending back to frontend
    UserModel.create(req.body)      //data coming from frontend are stored in req.body
    .then(users => res.json(users))
    .catch(err => res.json(err))
})

app.listen(3001, () => {
    console.log("server is running")
})
