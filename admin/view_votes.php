<?php
session_start();
require_once('../includes/db.php');

if(!isset($_SESSION['admin_id'])) {
    header('Location: login.php');
    exit();
}

$query = "SELECT v.id, u.name as voter_name, u.email as voter_email, 
          c.name as candidate_name, v.vote_time 
          FROM votes v 
          JOIN users u ON v.user_id = u.id 
          JOIN candidates c ON v.candidate_id = c.id 
          ORDER BY v.vote_time DESC";
$result = mysqli_query($conn, $query);
?>

<!DOCTYPE html>
<html>
<head>
    <title>View Votes - Admin</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <?php include('header.php'); ?>
    
    <div class="container">
        <h2>Voting Details</h2>
        
        <table border="1" cellpadding="10" style="width:100%; margin-top:20px;">
            <thead>
                <tr>
                    <th>Vote ID</th>
                    <th>Voter Name</th>
                    <th>Voter Email</th>
                    <th>Voted For</th>
                    <th>Vote Time</th>
                </tr>
            </thead>
            <tbody>
                <?php while($row = mysqli_fetch_assoc($result)): ?>
                <tr>
                    <td><?php echo $row['id']; ?></td>
                    <td><?php echo htmlspecialchars($row['voter_name']); ?></td>
                    <td><?php echo htmlspecialchars($row['voter_email']); ?></td>
                    <td><?php echo htmlspecialchars($row['candidate_name']); ?></td>
                    <td><?php echo $row['vote_time']; ?></td>
                </tr>
                <?php endwhile; ?>
            </tbody>
        </table>
    </div>
</body>
</html>
