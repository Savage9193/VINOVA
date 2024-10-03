import random
import smtplib

class AuthManager:
    def __init__(self):
        self.user_data = {
            "tyagi": "test", 
            "savage": "test",
        }
        self.otp = None

    def send_otp(self, email):
        """Send OTP to the user's email."""
        self.otp = random.randint(100000, 999999)  
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('tyagishahvez551@gmail.com', 'wsnxupoiushqpjjr') 
                message = f'Subject: Your OTP\n\nYour OTP is: {self.otp}'
                server.sendmail('tyagishahvez551@gmail', email, message) 
        except Exception as e:
            print(f"Error sending email: {e}")

    def login(self, username, password, email):
        """Handle user login and MFA."""
        if username in self.user_data and self.user_data[username] == password:
            self.send_otp(email)  
            return True 
        else:
            print("Invalid username or password.")
            return False

    def verify_otp(self, user_otp):
        """Verify the OTP entered by the user."""
        return str(self.otp) == user_otp
