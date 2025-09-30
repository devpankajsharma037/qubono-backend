from core.utils.emailSender import sendEmail

def verificationEmail(context):
    to = context['email']
    sendEmail('Activate your Qubono account verify your email!','email/verify.html',context,to)


def forgotEmail(context):
    to = context['email']
    sendEmail('Oops, Did You Forget Your Password?','email/forgot_password.html',context,to)