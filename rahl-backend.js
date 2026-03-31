const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { Configuration, OpenAIApi } = require('openai');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = process.env.PORT || 8000;

const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY
});
const openai = new OpenAIApi(configuration);

const MODE_PROMPTS = {
    royal: "You are a wise Royal Advisor. Answer in a royal, elegant style.",
    tech: "You are a Tech Guru. Answer in detailed, professional tech style.",
    creative: "You are a Creative Artist. Answer in imaginative, expressive style."
};

async function generateResponse(prompt, mode="royal") {
    const personality = MODE_PROMPTS[mode] || MODE_PROMPTS.royal;

    const textRes = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
            { role: "system", content: personality },
            { role: "user", content: prompt }
        ]
    });

    let responseText = `<text>${textRes.choices[0].message.content}</text>`;

    if (prompt.toLowerCase().includes("image")) {
        const imgRes = await openai.images.generate({
            model: "gpt-image-1",
            prompt: prompt,
            size: "512x512"
        });
        responseText += `<img>${imgRes.data[0].url}</img>`;
    }

    if (prompt.toLowerCase().includes("3d")) {
        responseText += `<3d>https://example.com/3dmodel.obj</3d>`;
    }

    return responseText;
}

app.post('/ai', async (req, res) => {
    const { prompt, mode } = req.body;
    if (!prompt) return res.status(400).json({ error: 'Prompt required' });

    try {
        const aiResponse = await generateResponse(prompt, mode);
        res.json({ response: aiResponse });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'AI generation failed' });
    }
});

app.listen(PORT, () => console.log(`RAHL-X backend running on port ${PORT}`));
