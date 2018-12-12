window.addEventListener('load', () => {

    file = null
    algorithm_select = document.getElementById('algorithm-select')
    textarea = document.getElementById('area')

    document.getElementById('file').addEventListener('change', () => {
        file = document.getElementById('file').files[0];
    });


    document.getElementById('encode').addEventListener('click', () => {
        if(algorithm_select.value == 'lsb')
        {
            data = new FormData()
            data.append('file', file)

            fetch(`/encode/lsb?msg=${textarea.value}`, {
                method: "POST",
                body: data
            }).then(
                response => response.json()
            ).then(
                val => {
                    if(val.Res == "OK")
                    {
                        document.location.href = `/download/${val.filename}`
                    }
                }
            )
        }
        else
        {
            console.log("Уупс :D");
        }
    });

    document.getElementById('decode').addEventListener('click', () => {
        if(algorithm_select.value == 'lsb') 
        {
            data = new FormData()
            data.append('file', file)

            fetch('/decode/lsb', {
                method: "POST",
                body: data
            }).then(
                response => response.json()
            ).then(
                val => {
                    if(val.Res == "OK")
                    {
                        document.location.href = `/download/${val.filename}`
                    }
                }
            )
        }
        else
        {
            console.log("Упс");
        }
    });
});