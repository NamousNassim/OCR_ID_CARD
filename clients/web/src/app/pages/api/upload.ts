import { NextApiRequest, NextApiResponse } from "next";
import * as mindee from "mindee";
import formidable from 'formidable';
import fs from "fs";

export const config = {
  api: {
    bodyParser: false, // Disable body parsing for file uploads
  },
};

const mindeeClient = new mindee.Client({ apiKey: "f022cfdc9ba73c5165d866f1907ea8e5" });

export default async (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === "POST") {
    const form = new formidable.IncomingForm();

    form.parse(req, async (err, fields, files) => {
      if (err) {
        console.error("Error parsing form:", err);
        res.status(500).json({ error: "Error parsing the form data." });
        return;
      }

      const file = Array.isArray(files.file) ? files.file[0] : files.file;

      if (!file || !file.filepath) {
        res.status(400).json({ error: "No file uploaded." });
        return;
      }

      const filePath = file.filepath;

      try {
        // Load and parse the file using Mindee
        const inputSource = mindeeClient.docFromPath(filePath);
        const response = await mindeeClient.enqueueAndParse(
          mindee.product.InternationalIdV2,
          inputSource
        );

        res.status(200).json(response.document); // Return parsed data
      } catch (error) {
        console.error("Error parsing document:", error);
        res.status(500).json({ error: "Error processing the file." });
      } finally {
        // Clean up temporary file
        fs.unlinkSync(filePath);
      }
    });
  } else {
    res.status(405).json({ error: "Method not allowed." });
  }
};