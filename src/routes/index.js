import express from 'express'
import SearchController from '../controllers/searchController.js'

const router = express.Router()
const searchController = new SearchController()

router.get('/', searchController.renderSearch)

router.get('/search', searchController.searchFluctuationStock)

export default router 