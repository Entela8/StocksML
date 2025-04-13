import { join, dirname } from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

class SearchController {
    searchFluctuationStock = async (req, res) => {
        const stockName = req.query.stockName;
        const fluctuationScript = join(__dirname, '../scripts', 'stockFluctuation.py');
        const newsScript = join(__dirname, '../scripts', 'getNews.py');

        console.log(`📈 Running fluctuation script for stock: ${stockName}`);
        const fluctuationProcess = spawnSync('python3', [
            fluctuationScript,
            JSON.stringify({ stockName })
        ]);

        console.log(`📰 Running news sentiment script for stock: ${stockName}`);
        const newsProcess = spawnSync('python3', [
            newsScript,
            JSON.stringify({ stockName })
        ]);

        // Parse outputs
        const fluctuationOutput = fluctuationProcess.stdout?.toString()?.trim();
        const fluctuationError = fluctuationProcess.stderr?.toString()?.trim();
        const fluctuationCode = fluctuationProcess.status;

        const newsOutput = newsProcess.stdout?.toString()?.trim();
        const newsError = newsProcess.stderr?.toString()?.trim();
        const newsCode = newsProcess.status;

        // Handle errors
        if (fluctuationCode !== 0 || newsCode !== 0) {
            return res.status(500).send({
                status: 500,
                message: 'Python script execution error',
                details: fluctuationError || newsError
            });
        }

        try {
            const fluctuationResult = JSON.parse(fluctuationOutput);
            const newsResult = JSON.parse(newsOutput);

            // 👇 Add news into result object
            fluctuationResult.news_sentiment = newsResult;

            res.render('search', { result: fluctuationResult });
        } catch (e) {
            console.error('❌ Failed to parse JSON:', e, fluctuationOutput, newsOutput);
            res.status(500).send({
                status: 500,
                message: 'Failed to parse Python output',
                details: e.toString()
            });
        }
    };

    renderSearch = (req, res) => {
        res.render('home');
    };

    renderResult = (req, res) => {
        // Not used right now
    };
}

export default SearchController;
