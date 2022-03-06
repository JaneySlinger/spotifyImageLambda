import { Construct } from "constructs";
import * as cdk from 'aws-cdk-lib';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as iam from "aws-cdk-lib/aws-iam";
import {PythonFunction} from "@aws-cdk/aws-lambda-python-alpha"
import path = require('path');

export class SpotifyLambda extends Construct {
    constructor(scope: Construct, id: string) {
        super(scope, id);

        const handler = new PythonFunction(this, "SpotifyLambdaFunction", {
            entry: path.join(__dirname, 'resources'),
            runtime: lambda.Runtime.PYTHON_3_9,
            timeout: cdk.Duration.seconds(15)
        });

        const api = new apigateway.RestApi(this,"spotify-api", {
            restApiName: "Spotify Lambda",
            description: "This service produces a pdf with merged image thumbnails."
        });

        const postlambdaIntegration = new apigateway.LambdaIntegration(handler, {
            requestTemplates: {"application/json": '{"statusCode": "200"}'}
        });

        api.root.addMethod("POST", postlambdaIntegration);
        

        const sendEmailsPolicy = new iam.PolicyStatement({
            actions: ['ses:SendRawEmail'],
            resources: ['arn:aws:ses:*'],
          });

        handler.role?.attachInlinePolicy(
            new iam.Policy(this, 'send-emails-policy', {
                statements: [sendEmailsPolicy],
            })
        )

    }
}