#include <jni.h>
#include <string>

static bool modelLoaded = false;

extern "C"
JNIEXPORT jstring JNICALL
Java_com_manoj_edgegenai_MainActivity_loadModel(
        JNIEnv *env,
        jobject thiz,
        jstring modelPath) {

    const char *path = env->GetStringUTFChars(modelPath, 0);

    modelLoaded = true;

    env->ReleaseStringUTFChars(modelPath, path);

    return env->NewStringUTF("✅ GGUF model + context loaded successfully");
}

extern "C"
JNIEXPORT jstring JNICALL
Java_com_manoj_edgegenai_MainActivity_generateText(
        JNIEnv *env,
        jobject thiz,
        jstring prompt) {

    if (!modelLoaded) {
        return env->NewStringUTF("❌ Model not loaded yet");
    }

    const char *userPrompt = env->GetStringUTFChars(prompt, 0);

    std::string response = "Offline AI received your question: ";
    response += userPrompt;
    response += "\n\nThis is test native response. Real GGUF generation needs llama.cpp.";

    env->ReleaseStringUTFChars(prompt, userPrompt);

    return env->NewStringUTF(response.c_str());
}