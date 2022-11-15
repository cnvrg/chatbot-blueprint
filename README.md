Use this blueprint with your custom data to train a tailored chatbot model and deploy an API endpoint which infers the intent of a customer message. To train this model, provide a dataset containing a collection of possible messages mapped to their intent.
This blueprint retrains a neural network on the custom dataset, resulting in a trained chatbot model and deployed endpoint to serve as an organization's virtual agent, which detects its customer intents and generates responses accordingly.

Complete the following steps to train this chatbot model:
1. Click the **Use Blueprint** button. The cnvrg Blueprint Flow page displays.
2. In the flow, click the **S3 Connector** task to display its dialog.
   * Within the **Parameters** tab, provide the following Key-Value pair information:
     - Key: `bucketname` - Value: enter the data bucket name
     - Key: `prefix` - Value: provide the main path to the data folder
   * Click the **Advanced** tab to change resources to run the blueprint, as required.
3. Return to the flow and click the **Train** task to display its dialog.
   * Within the **Parameters** tab, provide the S3-Connector path (Value) to the dataset for the `data` Key parameter.
   * Click the **Advanced** tab to change resources to run the blueprint, as required.
4. Click the **Run** button. The cnvrg software launches the training blueprint as set of experiments, generating a trained chatbot model and deploying it as a new API endpoint.
5. Track the blueprint’s real-time progress in its experiments page, which displays artifacts such as logs, metrics, hyperparameters, and algorithms.
6. Click the **Serving** tab in the project, locate your endpoint, and complete one or both of the following options:
   * Use the Try it Live section with any text to check the model to infer the intent.
   * Use the bottom integration panel to integrate your API with your code by copying in your code snippet.

A custom model and API endpoint which can infer the intents of customer messages have now been trained and deployed. To learn how this blueprint was created, click [here](https://github.com/cnvrg/chatbot-blueprint).
