import { Mail, Lock } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import logo from "/tce-logo.png";

function Login() {
  const prefersReducedMotion = useReducedMotion();

  const leftPanelVariants = {
    hidden: {
      opacity: 0,
      x: prefersReducedMotion ? 0 : 120,
    },
    visible: {
      opacity: 1,
      x: 0,
      transition: {
        duration: prefersReducedMotion ? 0 : 0.75,
        ease: [0.22, 1, 0.36, 1],
      },
    },
  };

  const formContainerVariants = {
    hidden: { opacity: 0, y: prefersReducedMotion ? 0 : 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: prefersReducedMotion ? 0 : 0.5,
        staggerChildren: prefersReducedMotion ? 0 : 0.1,
        delayChildren: prefersReducedMotion ? 0 : 0.15,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: prefersReducedMotion ? 0 : 16 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: prefersReducedMotion ? 0 : 0.45,
        ease: "easeOut",
      },
    },
  };

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-[3fr_2fr] bg-gray-100">

      {/* Right Panel */}
      <motion.div
  variants={leftPanelVariants}
  initial="hidden"
  animate="visible"
  className="order-1 md:order-2 bg-[url('/tce-bg.png')] bg-cover bg-center text-white flex flex-col justify-start items-start pt-20 px-12"
>

  <motion.h1
    variants={itemVariants}
    initial="hidden"
    animate="visible"
    transition={{ delay: prefersReducedMotion ? 0 : 0.2 }}
    className="mb-4 text-left"
  >
    <span className="block text-lg md:text-xl font-medium text-red-200">
      Welcome to
    </span>

    <span className="block text-3xl md:text-4xl font-bold leading-tight">
      Thiagarajar College of Engineering
    </span>
  </motion.h1>

</motion.div>

      {/* Left Panel */}
      <div className="order-2 md:order-1 flex items-center justify-center bg-gray-50 px-6 py-12 md:px-0 md:py-0">

        <motion.div
  variants={formContainerVariants}
  initial="hidden"
  animate="visible"
  className="w-full max-w-lg space-y-8"
>

  {/* TCE Accreditation Banner */}
  <motion.div
    variants={itemVariants}
    className="flex justify-center"
  >
    <img
      src="/tce-banner.png"
      alt="TCE Accreditation Banner"
      className="w-full max-w-lg object-contain"
    />
  </motion.div>

  {/* Login Card */}
  <Card className="border-red-100/80 shadow-[0_20px_45px_-35px_rgba(127,29,29,0.65)]">

    <CardHeader className="space-y-4">

      <motion.div variants={itemVariants} className="flex justify-center">
        <motion.img
          src={logo}
          alt="Logo"
          className="w-20 h-20 object-contain"
        />
      </motion.div>

      <motion.div variants={itemVariants} className="space-y-1">
        <CardTitle className="text-center text-3xl text-red-900">
          Welcome to TCE COAS
        </CardTitle>

        <p className="text-center text-sm text-red-800/80">
          Sign in to continue
        </p>
      </motion.div>

    </CardHeader>

    <CardContent className="space-y-6">

      <motion.div variants={itemVariants} className="space-y-2">
        <Label htmlFor="email" className="text-lg">Email</Label>

        <div className="login-input-motion flex items-center gap-3 rounded-lg border border-gray-200 bg-white px-4 py-2">
          <Mail size={22} className="text-gray-400" />
          <Input
            id="email"
            type="email"
            placeholder="Enter your email"
            className="border-0 p-0 text-lg shadow-none focus-visible:ring-0"
          />
        </div>
      </motion.div>

      <motion.div variants={itemVariants} className="space-y-2">
        <Label htmlFor="password"  className="text-lg">Password</Label>

        <div className="login-input-motion flex items-center gap-3 rounded-lg border border-gray-200 bg-white px-4 py-2">
          <Lock size={22} className="text-gray-400" />
          <Input
            id="password"
            type="password"
            placeholder="Enter your password"
            className="border-0 p-0 text-lg shadow-none focus-visible:ring-0"
          />
        </div>
      </motion.div>

      <motion.div variants={itemVariants}>
        <Button
          type="button"
          size="xl"
          className="login-button-motion w-full text-lg"
          asChild
        >
          <motion.button
            whileHover={prefersReducedMotion ? undefined : { y: -2, scale: 1.01 }}
            whileTap={prefersReducedMotion ? undefined : { y: 0, scale: 0.99 }}
          >
            Sign In
          </motion.button>
        </Button>
      </motion.div>

    </CardContent>

  </Card>

</motion.div>
      </div>

    </div>
  );
}

export default Login;