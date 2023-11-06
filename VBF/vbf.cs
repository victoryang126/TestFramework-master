using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

public class VBF
{
    public string Version { get; set; } = "0";
    public string Description { get; set; } = "";
    public string SwPart { get; set; } = "";
    public string SwPartType { get; set; } = "";
    public int Network { get; set; } = 0x00;
    public int DataFormatIdentifier { get; set; } = 0x00;
    public int EcuAddress { get; set; } = 0x00;
    public int VerificationBlockStart { get; set; } = 0x00;
    public string FrameFormat { get; set; } = "";
    public List<string[]> Erase { get; set; } = new List<string[]>();
    public byte[] Checksum { get; set; } = new byte[] { };
    public byte[] Raw { get; set; } = new byte[] { };
    public List<Tuple<int, byte[], byte[]>> Data { get; set; } = new List<Tuple<int, byte[], byte[]>>();

    public VBF(byte[] data)
    {
        if (data == null || data.Length == 0)
            throw new ArgumentException("Requires binary input");

        try
        {
            string dataString = Encoding.ASCII.GetString(data);
            int versionIndex = dataString.IndexOf("vbf_version");
            if (versionIndex != -1)
            {
                int endIndex = dataString.IndexOf('\n', versionIndex);
                string versionLine = dataString.Substring(versionIndex, endIndex - versionIndex);
                Version = versionLine.Split('=')[1].Replace(" ", "").Replace(";", "").Trim();
            }
            else
            {
                throw new Exception("Version not found");
            }

            string header = dataString.Substring(dataString.IndexOf("header"), dataString.IndexOf("\n}") - dataString.IndexOf("header") + 2);

            string desc = header.Substring(header.IndexOf("description ="), header.IndexOf("};") - header.IndexOf("description =")).Replace("//", ""); // remove comment lines if they exist
            Description = "";
            foreach (string line in desc.Split('\n'))
            {
                Description += line.Substring(line.IndexOf("\"") + 1, line.IndexOf("\",") - line.IndexOf("\"") - 1) + "\n";
            }

            header = header.Substring(header.IndexOf("sw_part_number"));

            bool erase = false;
            foreach (string line in header.Split('\n'))
            {
                string trimmedLine = line.Replace("\t", "").Replace("\r", "");
                if (trimmedLine.StartsWith("//"))
                {
                    continue;
                }

                if (trimmedLine.Contains("sw_part_number"))
                {
                    SwPart = trimmedLine.Substring(trimmedLine.IndexOf(" = ") + 3, trimmedLine.IndexOf("\";") - trimmedLine.IndexOf(" = ") - 3);
                    SwPart = SwPart.Replace(" ", "").Replace("\"", "");
                }
                else if (trimmedLine.Contains("sw_part_type"))
                {
                    SwPartType = trimmedLine.Substring(trimmedLine.IndexOf(" = ") + 3, trimmedLine.IndexOf(";") - trimmedLine.IndexOf(" = ") - 3);
                    SwPartType = SwPartType.Replace(" ", "").Replace("\"", "");
                }
                else if (trimmedLine.Contains("network"))
                {
                    Network = Convert.ToInt32(trimmedLine.Substring(trimmedLine.IndexOf(" = ") + 3, trimmedLine.IndexOf(";") - trimmedLine.IndexOf(" = ") - 3).Replace(" ", "").Replace("\"", ""));
                }
                else if (trimmedLine.Contains("data_format_identifier"))
                {
                    DataFormatIdentifier = Convert.ToInt32(trimmedLine.Substring(trimmedLine.IndexOf(" = ") + 3, trimmedLine.IndexOf(";") - trimmedLine.IndexOf(" = ") - 3).Replace(" ", "").Replace("\"", ""), 16);
                }
                else if (trimmedLine.Contains("ecu_address"))
                {
                    EcuAddress = Convert.ToInt32(trimmedLine.Substring(trimmedLine.IndexOf(" = 0x") + 5, trimmedLine.IndexOf(";") - trimmedLine.IndexOf(" = 0x") - 5).Replace(" ", "").Replace("\"", ""), 16);
                }
                else if (trimmedLine.Contains("verification_block_start"))
                {
                    VerificationBlockStart = Convert.ToInt32(trimmedLine.Substring(trimmedLine.IndexOf(" = 0x") + 5, trimmedLine.IndexOf(";") - trimmedLine.IndexOf(" = 0x") - 5).Replace(" ", "").Replace("\"", ""), 16);
                }
                else if (trimmedLine.Contains("frame_format"))
                {
                    FrameFormat = trimmedLine.Substring(trimmedLine.IndexOf(" = ") + 3, trimmedLine.IndexOf(";") - trimmedLine.IndexOf(" = ") - 3).Replace(" ", "").Replace("\"", "");
                }
                else if (trimmedLine.Contains("file_checksum"))
                {
                    // Implement the necessary conversion or handling for the checksum.
                    // Example: Checksum = Convert.FromBase64String(trimmedLine.Substring(trimmedLine.IndexOf(" = 0x") + 5, trimmedLine.IndexOf(";") - trimmedLine.IndexOf(" = 0x") - 5).Replace(" ", "").Replace("\"", ""));
                }
                else if (trimmedLine.Contains("erase = ") || erase)
                {
                    // Add your logic for parsing the erase data.
                    // Example: Erase.Add(new string[] { "0x123", "0x456" });
                    erase = true; // Handle multiline erase data
                    if (trimmedLine.Contains("};"))
                    {
                        erase = false;
                    }
                }
            }

            int binaryOffset = dataString.IndexOf("\n}") + 2;
            string binaryData = dataString.Substring(binaryOffset);
            Data = new List<Tuple<int, byte[], byte[]>>();

            while (binaryData.Length > 0)
            {
                int location = BitConverter.ToInt32(Encoding.ASCII.GetBytes(binaryData.Substring(0, 4)), 0);
                int size = BitConverter.ToInt32(Encoding.ASCII.GetBytes(binaryData.Substring(4, 4)), 0);
                byte[] blobData = Encoding.ASCII.GetBytes(binaryData.Substring(8, size));
                byte[] blobChecksum = Encoding.ASCII.GetBytes(binaryData.Substring(8 + size, 2));

                binaryData = binaryData.Substring(8 + size + 2);

                if (location != VerificationBlockStart)
                {
                    Data.Add(new Tuple<int, byte[], byte[]>(location, blobData, blobChecksum));
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            throw;
        }
    }
}
