<!DOCTYPE html>
<html>
    <head>
        <title>Login page</title>
        <link href="./login.css" rel="stylesheet">
    </head>
    <header>
    </header>
    <body class="changeme">
        <form action="login.php" method="post">
            <h2>
                Login here
            </h2>
            <h2>
                Hello <?php alert('hi'); ?>
            </h2>
            <div class="container">   
                <label>Username : </label>   
                <input type="text" placeholder="Enter Username" name="username" required>  
                <label>Password : </label>   
                <input type="password" placeholder="Enter Password" name="password" required>  
                <!-- <button type="submit">Login</button>   -->
                <input type="submit" value="Submit" class='submit'/>
            </div>   
        </form>>
        <script src="./login.js"></script>
    </body>
</html>