resource "kubernetes_namespace_v1" "fraud_detection" {
  metadata {
    name = "fraud-detection"
  }
}