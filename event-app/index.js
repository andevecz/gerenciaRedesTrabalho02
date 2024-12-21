const axios = require('axios');

async function checkPassword(password) {
    try {
        const response = await axios.post('http://localhost:5000/check_password', {
            password: password
        });

        console.log(`A senha foi encontrada em ${response.data.breaches} vazamentos.`);
    } catch (error) {
        console.error("Erro ao verificar a senha:", error.response ? error.response.data : error.message);
    }
}

checkPassword("12345");