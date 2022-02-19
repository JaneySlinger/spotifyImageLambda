import { lambda_layer_awscli } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigateway from "aws-cdk-lib/aws-apigateway";

export class SpotifyLambda extends Construct {
    constructor(scope: Construct, id: string) {
        super(scope, id);

        const handler = new lambda.Function(this, "SpotifyLambdaFunction", {
            runtime: lambda.Runtime.PYTHON_3_9,
            code: lambda.Code.fromAsset("resources"),
            handler: "lambda.lambda_handler"
        });

        const api = new apigateway.RestApi(this,"spotify-api", {
            restApiName: "Spotify Lambda",
            description: "This service produces a pdf with merged image thumbnails."
        });

        const postlambdaIntegration = new apigateway.LambdaIntegration(handler, {
            requestTemplates: {"application/json": '{"statusCode": "200"}'}
        });

        api.root.addMethod("POST", postlambdaIntegration);


    }
}