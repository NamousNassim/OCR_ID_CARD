// TODO Implement this library.
import 'dart:convert'; // Import pour convertir les données JSON
import 'package:http/http.dart' as http; // Import pour effectuer des requêtes HTTP

class ApiService {
  // URL de base de l'API
  final String baseUrl = "http://localhost:8000"; // Remplacez par l'URL de votre API

  // Méthode pour envoyer une image à l'API et récupérer les données
  Future<Map<String, dynamic>> fetchNationalCardData(String imagePath) async {
    var uri = Uri.parse('$baseUrl/extract-text/'); // Construire l'URL de l'endpoint
    var request = http.MultipartRequest('POST', uri); // Créer une requête POST multipart

    // Ajouter le fichier image à la requête
    request.files.add(await http.MultipartFile.fromPath('file', imagePath));

    // Envoyer la requête
    var response = await request.send();

    // Vérifier le statut de la réponse
    if (response.statusCode == 200) {
      var responseData = await response.stream.bytesToString(); // Lire les données de la réponse
      return json.decode(responseData); // Décoder et retourner les données JSON
    } else {
      throw Exception('Erreur lors du traitement de la requête : ${response.statusCode}'); // Gérer les erreurs
    }
  }
}

