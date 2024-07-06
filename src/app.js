import express from 'express'
import routes from './routes/index.js'

const app = express()

app.set('view engine', 'ejs');
app.set('views', 'src/views'); 

app.use(express.static('public'))
app.use('/', routes)

const port = 9000

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})