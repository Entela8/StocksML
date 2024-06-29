import express from 'express'
import HelloController from '../controllers/helloController.js'
const router = express.Router()
const helloController = new HelloController()

router.get('/hello', helloController.hello)

export default router 