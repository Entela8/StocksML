import { join, dirname } from "path";
import { spawnSync } from "child_process";
import { readFile } from "fs/promises";
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

class SearchController {

    searchStock = async (req, res) => {
        const stockName = req.query.stockName;
        const scriptPath = join(__dirname, '../scripts', 'stockFluctuation.py');

        console.log(`Executing Python script for stock: ${stockName}`);

        const pythonProcess = spawnSync('python3', [
            scriptPath,
            JSON.stringify({ stockName })
        ]);

        const result = pythonProcess.stdout?.toString()?.trim();
        const error = pythonProcess.stderr?.toString()?.trim();
        const exitCode = pythonProcess.status;

        console.log('Python script output:', result);
        console.log('Python script error output:', error);
        console.log('Python script exit code:', exitCode);

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
            res.status(500).send({ status: 500, message: 'Server error', details: 'Failed to parse JSON' });
        }
    }

    renderSearch = (req, res) => {
        res.render('home');
    }

    renderResult = (req, res) => {

    }
}

export default SearchController;
