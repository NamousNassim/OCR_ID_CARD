import 'package:flutter/material.dart';
import '../widgets/custom_button.dart';

class WelcomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Welcome'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Welcome to the App!',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            CustomButton(
              text: 'Login',
              onPressed: () {
                Navigator.pushNamed(context, '/login');
              },
            ),
            CustomButton(
              text: 'Register',
              onPressed: () {
                Navigator.pushNamed(context, '/register');
              },
            ),
          ],
        ),
      ),
    );
  }
}