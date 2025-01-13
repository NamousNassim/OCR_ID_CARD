import 'package:flutter/material.dart'; // Importation du package Flutter pour créer des widgets
import 'package:image_picker/image_picker.dart'; // Importation du package pour accéder à la caméra et à la galerie
import 'package:mobile/screens/dashboard_screen.dart';
import 'dart:io'; // Permet de travailler avec des fichiers locaux
import 'api_service.dart'; // Importation du service API personnalisé
// ignore: duplicate_import
import 'dashboard_screen.dart'; // Importation de l'écran du tableau de bord

class FormScreen extends StatefulWidget {
  @override
  _FormScreenState createState() => _FormScreenState(); // Crée un état mutable pour le widget FormScreen
}

class _FormScreenState extends State<FormScreen> {
  final _formKey = GlobalKey<FormState>(); // Clé globale pour gérer la validation du formulaire

  // Contrôleurs pour gérer le texte des champs du formulaire
  final _countryController = TextEditingController();
  final _documentTypeController = TextEditingController();
  final _lastNameController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _birthDateController = TextEditingController();
  final _birthPlaceController = TextEditingController();
  final _idNumberController = TextEditingController();
  final _canNumberController = TextEditingController();
  final _expiryDateController = TextEditingController();
  final _additionalInfoController = TextEditingController();

  File? _selectedImage; // Variable pour stocker l'image sélectionnée

  final ImagePicker _picker = ImagePicker(); // Instance pour interagir avec la caméra et la galerie
  final ApiService _apiService = ApiService(); // Instance du service API pour appeler les endpoints

  // Fonction pour sélectionner une image à partir de la caméra ou de la galerie
  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await _picker.pickImage(source: source); // Ouvre l'interface pour choisir une image

    if (pickedFile != null) { // Vérifie si une image a été sélectionnée
      setState(() {
        _selectedImage = File(pickedFile.path); // Stocke l'image sélectionnée
      });
      await _processImage(); // Lance le traitement de l'image
    }
  }

  // Fonction pour traiter l'image et appeler l'API
  Future<void> _processImage() async {
    if (_selectedImage != null) { // Vérifie si une image est disponible
      try {
        var data = await _apiService.fetchNationalCardData(_selectedImage!.path); // Appelle l'API pour extraire les données

        // Remplit les champs du formulaire avec les données récupérées
        setState(() {
          _countryController.text = data['country'] ?? ''; // Remplit le champ "Country"
          _documentTypeController.text = data['document_type'] ?? ''; // Remplit le champ "Document Type"
          _lastNameController.text = data['last_name'] ?? ''; // Remplit le champ "Last Name"
          _firstNameController.text = data['first_name'] ?? ''; // Remplit le champ "First Name"
          _birthDateController.text = data['birth_date'] ?? ''; // Remplit le champ "Birth Date"
          _birthPlaceController.text = data['birth_place'] ?? ''; // Remplit le champ "Birth Place"
          _idNumberController.text = data['id_number'] ?? ''; // Remplit le champ "ID Number"
          _canNumberController.text = data['can_number'] ?? ''; // Remplit le champ "CAN Number"
          _expiryDateController.text = data['expiry_date'] ?? ''; // Remplit le champ "Expiry Date"
          _additionalInfoController.text = data['additional_info'] ?? ''; // Remplit le champ "Additional Info"
        });
      } catch (e) { // Capture les erreurs de l'API
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: ${e.toString()}')), // Affiche un message d'erreur
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('National Card Form'), // Titre de la barre d'application
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0), // Définit la marge intérieure du formulaire
        child: Form(
          key: _formKey, // Associe la clé de formulaire pour la validation
          child: SingleChildScrollView(
            child: Column(
              children: [
                if (_selectedImage != null) // Vérifie si une image est disponible
                  Image.file(_selectedImage!, height: 200, width: 200), // Affiche l'image sélectionnée

                // Champs de formulaire pour les informations personnelles
                TextFormField(
                  controller: _countryController, // Champ "Country"
                  decoration: InputDecoration(labelText: 'Country'),
                ),
                TextFormField(
                  controller: _documentTypeController, // Champ "Document Type"
                  decoration: InputDecoration(labelText: 'Document Type'),
                ),
                TextFormField(
                  controller: _lastNameController, // Champ "Last Name"
                  decoration: InputDecoration(labelText: 'Last Name'),
                ),
                TextFormField(
                  controller: _firstNameController, // Champ "First Name"
                  decoration: InputDecoration(labelText: 'First Name'),
                ),
                TextFormField(
                  controller: _birthDateController, // Champ "Birth Date"
                  decoration: InputDecoration(labelText: 'Birth Date'),
                ),
                TextFormField(
                  controller: _birthPlaceController, // Champ "Birth Place"
                  decoration: InputDecoration(labelText: 'Birth Place'),
                ),
                TextFormField(
                  controller: _idNumberController, // Champ "ID Number"
                  decoration: InputDecoration(labelText: 'ID Number'),
                ),
                TextFormField(
                  controller: _canNumberController, // Champ "CAN Number"
                  decoration: InputDecoration(labelText: 'CAN Number'),
                ),
                TextFormField(
                  controller: _expiryDateController, // Champ "Expiry Date"
                  decoration: InputDecoration(labelText: 'Expiry Date'),
                ),
                TextFormField(
                  controller: _additionalInfoController, // Champ "Additional Info"
                  decoration: InputDecoration(labelText: 'Additional Info'),
                ),
                SizedBox(height: 20), // Espacement vertical

                // Boutons pour ouvrir la caméra ou la galerie
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly, // Aligne les boutons horizontalement
                  children: [
                    ElevatedButton(
                      onPressed: () => _pickImage(ImageSource.camera), // Ouvre la caméra
                      child: Text('Open Camera'),
                    ),
                    ElevatedButton(
                      onPressed: () => _pickImage(ImageSource.gallery), // Ouvre la galerie
                      child: Text('Open Gallery'),
                    ),
                  ],
                ),
                SizedBox(height: 20), // Espacement vertical

                // Bouton pour naviguer vers le tableau de bord
                ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) { // Vérifie la validation du formulaire
                      // Préparer les données pour le tableau de bord
                      Map<String, String> profileData = {
                        "Country": _countryController.text,
                        "Document Type": _documentTypeController.text,
                        "Last Name": _lastNameController.text,
                        "First Name": _firstNameController.text,
                        "Birth Date": _birthDateController.text,
                        "Birth Place": _birthPlaceController.text,
                        "ID Number": _idNumberController.text,
                        "CAN Number": _canNumberController.text,
                        "Expiry Date": _expiryDateController.text,
                        "Additional Info": _additionalInfoController.text,
                      };

                      // Naviguer vers le tableau de bord
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              DashboardScreen(profileData: profileData),
                        ),
                      );
                    }
                  },
                  child: Text('Save Profile'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
