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
    $name = mysqli_real_escape_string($conn, $_POST['name']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $mobile = mysqli_real_escape_string($conn, $_POST['mobile']);
    
    $query = "UPDATE users SET name='$name', email='$email', mobile='$mobile' WHERE id=$user_id";
    if(mysqli_query($conn, $query)) {
        $message = "User updated successfully!";
    } else {
        $message = "Error updating user.";
    }
}

$query = "SELECT * FROM users WHERE id=$user_id";
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
    <title>Edit User - Admin</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <?php include('header.php'); ?>
    
    <div class="container">
        <h2>Edit User</h2>
        
        <?php if($message): ?>
            <p style="color: green;"><?php echo $message; ?></p>
        <?php endif; ?>
        
        <form method="POST" style="max-width: 500px;">
            <div style="margin-bottom: 15px;">
                <label>Name:</label><br>
                <input type="text" name="name" value="<?php echo htmlspecialchars($user['name']); ?>" required style="width: 100%; padding: 8px;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label>Email:</label><br>
                <input type="email" name="email" value="<?php echo htmlspecialchars($user['email']); ?>" required style="width: 100%; padding: 8px;">
            </div>
            
            <div style="margin-bottom: 15px;">
                <label>Mobile:</label><br>
                <input type="text" name="mobile" value="<?php echo htmlspecialchars($user['mobile']); ?>" required style="width: 100%; padding: 8px;">
            </div>
            
            <button type="submit" style="padding: 10px 20px;">Update User</button>
            <a href="manage_users.php" style="margin-left: 10px;">Back to List</a>
        </form>
    </div>
</body>
</html>
