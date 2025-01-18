import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/foundation.dart' show kIsWeb;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Upload an ID',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: UploadPage(),
    );
  }
}

class UploadPage extends StatefulWidget {
  @override
  _UploadPageState createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  File? _imageFile;
  Uint8List? _webImage;
  bool _isLoading = false;
  Map<String, dynamic>? _apiResponse;

  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await ImagePicker().pickImage(source: source);

    if (pickedFile != null) {
      if (kIsWeb) {
        final webImage = await pickedFile.readAsBytes();
        setState(() {
          _webImage = webImage;
        });
      } else {
        setState(() {
          _imageFile = File(pickedFile.path);
        });
      }
    } else {
      print('No image selected.');
    }
  }

  Future<void> _uploadImage() async {
    if (_imageFile == null && _webImage == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Please upload a file before submitting.')));
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('https://api.mindee.net/v1/products/mindee/international_id/v2/predict_async'),
      );
      request.headers['Authorization'] = 'Token f022cfdc9ba73c5165d866f1907ea8e5';

      if (kIsWeb) {
        request.files.add(http.MultipartFile.fromBytes('document', _webImage!, filename: 'upload.png'));
      } else {
        request.files.add(await http.MultipartFile.fromPath('document', _imageFile!.path));
      }

      final response = await request.send();
      final responseData = await http.Response.fromStream(response);
      final data = json.decode(responseData.body);
      print('POST response: $data');
      final jobId = data['job']['id'];

      // Polling function to check job status
      Future<void> checkJobStatus() async {
        final statusResponse = await http.get(
          Uri.parse('https://api.mindee.net/v1/products/mindee/international_id/v2/documents/queue/$jobId'),
          headers: {'Authorization': 'Token f022cfdc9ba73c5165d866f1907ea8e5'},
        );

        final statusData = json.decode(statusResponse.body);
        print('GET response: $statusData');

        if (statusData['job']['status'] == 'completed') {
          setState(() {
            _apiResponse = statusData;
            _isLoading = false;
          });
        } else {
          Future.delayed(Duration(seconds: 5), checkJobStatus); // Retry after 5 seconds
        }
      }

      checkJobStatus();
    } catch (error) {
      print('Error uploading the file: $error');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Upload an ID'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              if (_imageFile != null)
                Image.file(_imageFile!, height: 200)
              else if (_webImage != null)
                Image.memory(_webImage!, height: 200)
              else
                Text('No image selected.'),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => _pickImage(ImageSource.gallery),
                child: Text('Pick Image from Gallery'),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => _pickImage(ImageSource.camera),
                child: Text('Take a Photo'),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _isLoading ? null : _uploadImage,
                child: _isLoading ? CircularProgressIndicator() : Text('Submit'),
              ),
              SizedBox(height: 20),
              if (_apiResponse != null && _apiResponse!['document'] != null && _apiResponse!['document']['inference'] != null)
                Expanded(
                  child: ListView(
                    children: [
                      Text('Country: ${_apiResponse!['document']['inference']['prediction']['country_of_issue']['value'] ?? ''}'),
                      Text('Document Type: ${_apiResponse!['document']['inference']['prediction']['document_type']['value'] ?? ''}'),
                      Text('Last Name: ${(_apiResponse!['document']['inference']['prediction']['surnames'] as List).map((surname) => surname['value']).join(', ') ?? ''}'),
                      Text('First Name: ${(_apiResponse!['document']['inference']['prediction']['given_names'] as List).map((name) => name['value']).join(', ') ?? ''}'),
                      Text('Birth Date: ${_apiResponse!['document']['inference']['prediction']['birth_date']['value'] ?? ''}'),
                      Text('Birth Place: ${_apiResponse!['document']['inference']['prediction']['birth_place']['value'] ?? ''}'),
                      Text('ID Number: ${_apiResponse!['document']['inference']['prediction']['document_number']['value'] ?? ''}'),
                      Text('CAN Number: ${_apiResponse!['document']['inference']['prediction']['personal_number']['value'] ?? ''}'),
                      Text('Expiry Date: ${_apiResponse!['document']['inference']['prediction']['expiry_date']['value'] ?? ''}'),
                      Text('Additional Info: ${_apiResponse!['document']['inference']['prediction']['additional_info'] ?? ''}'),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}