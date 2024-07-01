import { join, dirname } from "path";
import { spawnSync } from "child_process";
import { readFile } from "fs/promises";
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

class SearchController {

    searchStock = async (req, res) => {
        const stockName = req.query.stockName;
        const scriptPath = join(__dirname, '../scripts', 'stockFluctuation.py');
        const resultsPath = join(__dirname, '../scripts', 'results.json');

        const pythonProcess = spawnSync('python3', [
            scriptPath,
            JSON.stringify({ stockName })
        ]);

        const result = pythonProcess.stdout?.toString()?.trim();
        const error = pythonProcess.stderr?.toString()?.trim();

        if (error) {
            console.log(error);
            res.status(500).send({ status: 500, message: 'Server error' });
            return;
        }

        try {
            const resultParsed = JSON.parse(result);
            res.send(resultParsed);
        } catch (e) {
            console.error('Failed to parse JSON:', e);
            res.status(500).send({ status: 500, message: 'Server error' });
        }
    }

    renderSearch = (req, res) => {
        res.render('home');
    }
}

export default SearchController;
