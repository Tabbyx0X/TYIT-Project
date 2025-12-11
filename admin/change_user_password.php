<?php
session_start();
require_once('../includes/db.php');

if(!isset($_SESSION['admin_id'])) {
    header('Location: login.php');
    exit();
}

$user_id = $_GET['id'] ?? 0;
$message = '';

if($_SERVER['REQUEST_METHOD'] == 'POST') {
    $new_password = $_POST['new_password'];
    $confirm_password = $_POST['confirm_password'];
    
    if($new_password === $confirm_password) {
        $hashed_password = password_hash($new_password, PASSWORD_DEFAULT);
        $query = "UPDATE users SET password='$hashed_password' WHERE id=$user_id";
        
        if(mysqli_query($conn, $query)) {
            $message = "Password changed successfully!";
        } else {
            $message = "Error changing password.";
        }
    } else {
        $message = "Passwords do not match!";
    }
}

$query = "SELECT name, email FROM users WHERE id=$user_id";
$result = mysqli_query($conn, $query);
$user = mysqli_fetch_assoc($result);

if(!$user) {
    header('Location: manage_users.php');
    exit();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Change User Password - Admin</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <?php include('header.php'); ?>
    
    <div class="container">
        <h2>Change Password for <?php echo htmlspecialchars($user['name']); ?></h2>
        <p>Email: <?php echo htmlspecialchars($user['email']); ?></p>
        
        <?php if($message): ?>
            <p style="color: <?php echo strpos($message, 'success') ? 'green' : 'red'; ?>;">
                <?php echo $message; ?>
            </p>
        <?php endif; ?>
        
        <form method="POST" style="max-width: 500px;">
            <div style="margin-bottom: 15px;">
                <label>New Password:</label><br>
                <input type="password" name="new_password" required style="width: 100%; padding: 8px;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label>Confirm Password:</label><br>
                <input type="password" name="confirm_password" required style="width: 100%; padding: 8px;">
            </div>
            
            <button type="submit" style="padding: 10px 20px;">Change Password</button>
            <a href="manage_users.php" style="margin-left: 10px;">Back to List</a>
        </form>
    </div>
</body>
</html>
