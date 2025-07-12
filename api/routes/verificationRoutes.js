const express = require("express");
const {
    verifyFarmer,
    getVerificationStatus,
    requestManualVerification,
    getVerificationStats
} = require("../controllers/verificationController");
const { verifyToken, isFarmer, isAdmin } = require("../utils/authMiddleware");

const router = express.Router();

// Farmer verification routes
router.post("/verify-farmer", verifyToken, isFarmer, verifyFarmer);
router.get("/status", verifyToken, isFarmer, getVerificationStatus);
router.post("/manual-request", verifyToken, isFarmer, requestManualVerification);

// Admin routes
router.get("/stats", verifyToken, isAdmin, getVerificationStats);

module.exports = router;
