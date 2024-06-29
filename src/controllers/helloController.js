class HelloController {
    hello = (req, res) => 
    {
        res.render('home', {name: 'entela'})
    }
}

export default HelloController