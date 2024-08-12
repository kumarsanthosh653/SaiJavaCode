<!DOCTYPE html>
<html>
<head>
    <title>Minfy Team</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
        }
        h1 {
            color: #003366;
        }
        .version-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .version {
            margin: 0 15px;
            text-align: center;
        }
        h2 {
            margin-bottom: 10px;
        }
        h2.version1 {
            color: #008000;
        }
        h2.version2 {
            color: #ff0000;
        }
        h2.version3 {
            color: #800080;
        }
        .thank-you {
            display: none;
            color: #ffa500;
            font-size: 1.5em;
            margin-top: 20px;
        }
        button {
            margin-top: 30px;
            padding: 10px 20px;
            font-size: 1em;
            color: white;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
    <script>
        function showThankYouMessage() {
            document.getElementById('thankYouMsg').style.display = 'block';
        }
    </script>
</head>
<body>
    <h1>Hello Value Momentum Team!!</h1>
    
    <div class="version-container">
        <div class="version">
            <h2 class="version1">This is Version1</h2>
            <img src="https://via.placeholder.com/150?text=Person1" alt="Person representing Version 1">
        </div>
        
        <div class="version">
            <h2 class="version2">This is Version2</h2>
            <img src="https://via.placeholder.com/150?text=Person2" alt="Person representing Version 2">
        </div>
        
        <div class="version">
            <h2 class="version3">This is Version3</h2>
            <img src="https://via.placeholder.com/150?text=Person3" alt="Person representing Version 3">
        </div>
    </div>
    
    <button onclick="showThankYouMessage()">Press me</button>
    <div id="thankYouMsg" class="thank-you">Thank you!</div>
</body>
</html>
