import { join, dirname } from "path";
import { spawnSync } from "child_process";
import { readFile } from "fs/promises";
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

class SearchController {

    searchFluctuationStock = async (req, res) => {
        const stockName = req.query.stockName;
        const scriptPath = join(__dirname, '../scripts', 'stockFluctuation.py');

        console.log(`Executing Python script for stock: ${stockName}`);

        const pythonProcess = spawnSync('python3', [
            scriptPath,
            JSON.stringify({ stockName })
        ]);

        const result = pythonProcess.stdout?.toString()?.trim();
        console.dir(result)
        const error = pythonProcess.stderr?.toString()?.trim();
        const exitCode = pythonProcess.status;

        if (exitCode !== 0) {
            res.status(500).send({ status: 500, message: 'Python script execution error', details: error });
            return;
        }

        if (!result) {
            res.status(500).send({ status: 500, message: 'No output from Python script' });
            return;
        }

        try {
            const resultParsed = JSON.parse(result);
            res.render('search', { result: resultParsed });
        } catch (e) {
            console.error('Failed to parse JSON:', e, result);
            res.status(500).send({ status: 500, message: 'Server error', details: e.error });
        }
    }

    renderSearch = (req, res) => {
        res.render('home');
    }

    renderResult = (req, res) => {

    }
}

export default SearchController;
