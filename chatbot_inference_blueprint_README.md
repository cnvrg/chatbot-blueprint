Use this blueprint to immediately infer the intent of a customer message. To run this pretrained intent recognition model, create a ready-to-use API endpoint that can be quickly integrated with your data and application.
This inference blueprint's model was trained using e-commerce data. To use custom data according to your specific business, run this counterpart’s [training blueprint](../chatbot-blueprint/README.md), which trains the model and establishes an endpoint based on the newly trained model.
This blueprint supports two modes:
- `intent` - returns the intent of the given text
- `response` - returns a response message relevant to the identified intent based on a intent-response dictionary provided in the environment variable `responses_file`
 Define the intent/response mode in the `mode` environment variable.

Complete the following steps to deploy this chatbot API endpoint:
1. Click the **Use Blueprint** button. The cnvrg Blueprint Flow page displays.
2.	In the dialog, select the relevant compute to deploy API endpoint and click the **Start** button.
3. The cnvrg software redirects to your endpoint. Complete one or both of the following options:
   * Use the Try it Live section with any text to check the model to infer the intent.
   * Use the bottom integration panel to integrate your API with your code by copying in your code snippet.

An API endpoint that infers the intents of customer messages has now been deployed. To learn how this blueprint was created, click [here](https://github.com/cnvrg/chatbot-blueprint).
