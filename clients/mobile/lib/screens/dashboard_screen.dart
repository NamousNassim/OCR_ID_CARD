import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  final Map<String, String> profileData; // Données du profil à afficher

  DashboardScreen({required this.profileData}); // Constructeur pour passer les données du profil

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Profile Dashboard'), // Titre du tableau de bord
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0), // Marges autour du contenu
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start, // Aligne les éléments à gauche
          children: [
            Text(
              'Profile Information',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold), // Style du titre principal
            ),
            SizedBox(height: 20), // Espacement vertical

            // Affiche chaque donnée du profil sous forme de liste
            Expanded(
              child: ListView.builder(
                itemCount: profileData.length, // Nombre de données dans le profil
                itemBuilder: (context, index) {
                  String key = profileData.keys.elementAt(index); // Clé actuelle (nom du champ)
                  String value = profileData[key]!; // Valeur associée

                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8.0), // Espacement entre les éléments
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "$key:",
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                          ), // Nom du champ en gras
                        ),
                        SizedBox(width: 8), // Espacement horizontal
                        Expanded(
                          child: Text(value), // Valeur du champ
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),

            SizedBox(height: 20), // Espacement vertical

            // Bouton pour retourner à l'écran précédent
            Center(
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pop(context); // Retour à l'écran précédent
                },
                child: Text('Go Back'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
